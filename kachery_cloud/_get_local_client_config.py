from ast import mod
import os
import yaml
from .get_kachery_cloud_dir import get_kachery_cloud_dir


_global = {
    'config': None
}

def _get_local_client_config():
    config = _global['config']
    if config is None:
        fname = f'{get_kachery_cloud_dir()}/config.yaml'
        config = {}
        if os.path.exists(fname):
            with open(fname, 'r') as f:
                config = yaml.safe_load(f)
        modified = False
        # if 'multiuser' not in config:
        #     config['multiuser'] = False
        #     modified = True
        if modified:
            with open(fname, 'w') as f:
                yaml.safe_dump(config, f)
        _global['config'] = config
    return config