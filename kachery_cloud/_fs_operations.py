import os
import stat
from ._get_local_client_config import _get_local_client_config


all_dir_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH
all_file_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH

def _makedirs(path: str):
    config = _get_local_client_config()
    # multiuser = config['multiuser']
    # if multiuser:
    #     os.makedirs(path, mode=all_dir_mode)
    # else:
    #     os.makedirs(path)
    os.makedirs(path)

def _chmod_dir(path: str):
    raise Exception('Should not be used')
    # config = _get_local_client_config()
    # multiuser = config['multiuser']
    # if multiuser:
    #     os.chmod(path, mode=all_dir_mode)

def _chmod_file(path: str):
    raise Exception('Should not be used')
    # config = _get_local_client_config()
    # multiuser = config['multiuser']
    # if multiuser:
    #     os.chmod(path, mode=all_file_mode)