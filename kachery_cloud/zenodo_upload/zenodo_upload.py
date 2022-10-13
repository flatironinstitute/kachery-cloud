import os
from typing import Any
import requests
import json

from ..load_file import load_file
from ..store_file_local import store_file_local, store_json_local


class ZenodoUploader:
    def __init__(self, *,
        author: str,
        affiliation: str,
        title: str,
        description: str,
        sandbox: bool=True
    ) -> None:
        self._author = author
        self._affiliation = affiliation
        self._title = title
        self._description = description
        self._sandbox = sandbox
        self._base_zenodo_url = 'https://sandbox.zenodo.org' if sandbox else 'https://zenodo.org'
        env_name = 'ZENODO_SANDBOX_ACCESS_TOKEN' if sandbox else 'ZENODO_ACCESS_TOKEN'
        try:
            self._access_token = os.environ[env_name]
        except:
            raise Exception(f'Environment variable not set: {env_name}')
        
        # create a new deposition
        print('Creating new deposition...')
        headers = {"Content-Type": "application/json"}
        r2 = requests.post(
            f'{self._base_zenodo_url}/api/deposit/depositions',
            params={'access_token': self._access_token},
            json={},
            headers=headers
        )
        if r2.status_code not in [200, 201]:
            raise Exception(f'Problem creating deposition: {r2.status_code}')

        # get the deposition ID
        self._deposition_id = r2.json()['id']
        print(f'Deposition ID: {self._deposition_id}')

        # get the bucket url
        self._bucket_url = r2.json()["links"]["bucket"]
        print(f'Bucket URL: {self._bucket_url}')
    def upload_file(self, uri: str, *, name: str):
        path = load_file(uri)
        print(f'Uploading {name}...')
        with open(path, 'rb') as ff:
            r3 = requests.put(
                f'{self._bucket_url}/{name}',
                params={'access_token': self._access_token},
                data=ff
            )
            if r3.status_code not in [200, 201]:
                raise Exception(f'Problem uploading file: {r3.status_code}')
        return f'{"zenodo-sandbox" if self._sandbox else "zenodo"}://{self._deposition_id}/{name}'
    def upload_file_recursive(self, uri: str, *, name: str):
        print(f'Uploading recursive {name}: {uri}')
        file_path = load_file(uri)
        if file_path is None:
            raise Exception(f'Unable to load {uri}')
        try:
            with open(file_path, 'r') as ff:
                file_obj = json.load(ff)
        except:
            file_obj = None
            print(f'Warning: unable to load json from file: {uri}')
        if file_obj is not None:
            file_obj_processed = self._upload_file_recursive_process_obj(file_obj)
            uri2 = store_json_local(file_obj_processed)
            return self.upload_file(uri2, name=name)
        else:
            return self.upload_file(uri, name=name)
    def _upload_file_recursive_process_obj(self, x: Any):
        if isinstance(x, dict):
            ret = {}
            for k, v in x.items():
                ret[k] = self._upload_file_recursive_process_obj(v)
            return ret
        elif isinstance(x, list):
            ret = []
            for i in range(len(x)):
                ret.append(self._upload_file_recursive_process_obj(x[i]))
            return ret
        elif isinstance(x, str):
            if x.startswith('sha1://') or x.startswith('zenodo://') or x.startswith('zenodo-sandbox://'):
                uri0 = store_file_local(x) # make sure it's a sha-1 url
                sha1 = uri0.split('?')[0].split('/')[2]
                return self.upload_file_recursive(x, name=sha1)
            else:
                return x
        else:
            return x
    def finalize_upload(self):
        data = {
            'metadata': {
                'title': self._title,
                'upload_type': 'dataset',
                'description': self._description,
                'creators': [{'name': self._author, 'affiliation': self._affiliation}]
            }
        }
        # put the meta data
        print('Uploading metadata')
        headers = {"Content-Type": "application/json"}
        r4 = requests.put(
            f'{self._base_zenodo_url}/api/deposit/depositions/{self._deposition_id}',
            params={'access_token': self._access_token},
            data=json.dumps(data),
            headers=headers
        )
        if r4.status_code not in [200, 201]:
            raise Exception(f'Problem uploading metadata: {r4.status_code}')
        rr = r4.json()
        links = rr['links']
        latest_draft_html = links['latest_draft_html']
        print('')
        print(f'IMPORTANT: You must visit this link to finalize the upload:')
        print(f'{latest_draft_html}')
        input('ZENODO UPLOAD: Once you have visited the above link and published this zenodo upload, press enter to continue. ')

def initiate_zenodo_upload(*,
    author: str,
    affiliation: str,
    title: str,
    description: str,
    sandbox: bool=True
):  
    uploader = ZenodoUploader(
        author=author,
        affiliation=affiliation,
        title=title,
        description=description,
        sandbox=sandbox
    )
    return uploader
    

