from typing import Union
import os
from kachery_cloud.TaskBackend import TaskBackend
import kachery_cloud as kcl


# This backend service
# will listen for requests on remote computers to upload files
# that are stored locally.
#
# You can store some content locally via
# uri = kcl.store_text_local('random-text-00001')
# Now this file is stored locally but not in the cloud
# On a remote computer you can send a request to upload
# the file. See the file_share_remote_test.py example
# and paste in the desired url and the project ID
# for this backend.

# uri is obtained from kcl.store_*_local(fname) on this computer
def _kachery_store_shared_file(*, uri: str):
    """uploads the shared file when requested. Note that the uri must be sent by the task on the client
    Parameters
    ----------
    uri : str
        the uri for the file
    Raises
    ------
    Exception
        Raises Unable to load file if file can't be loaded
    """
    # impose restrictions on uri here
    if uri != '' and uri is not None:
        if uri.startswith('sha1://'):
            fname = kcl.load_file(uri, local_only=True) # requires kachery-cloud >= 0.1.19
            if fname is not None:
                print(f'storing {fname} in cloud')
                kcl.store_file(fname)
            else:
                raise Exception(f'Unable to load file: {uri}')
        elif uri.startswith('sha1-enc://'):
            # Important not to share files from encrypted URIs
            # This is how we restrict access
            raise Exception('Cannot share file from encrypted URI')
        else:
            raise Exception(f'Unexpected uri: {uri}')
    else:
        raise Exception(f'Invalid uri: {uri}')

def _start_backend(*, project_id: Union[str, None]=None):
    X = TaskBackend(project_id=project_id)
    X.register_task_handler(
        task_type='action',
        task_name='kachery_store_shared_file.1',
        task_function=_kachery_store_shared_file
    )
    print('Sharing local files')

    # Backend will listen for requests to upload a file to kachery cloud
    X.run()

def share_local_files_experimental(*, project_id: Union[str, None]=None):
    _start_backend(project_id=project_id)