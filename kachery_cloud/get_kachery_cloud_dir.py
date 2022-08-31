import os
import random
import atexit
import shutil

def use_sandbox(use: bool=True):
    if use:
        os.environ['KACHERY_CLOUD_USE_SANDBOX'] = '1'
        if not os.path.exists(os.environ['KACHERY_CLOUD_SANDBOX_DIR']):
            # only create the dir when we are actually switching to sandbox mode
            os.makedirs(os.environ['KACHERY_CLOUD_SANDBOX_DIR'])
            # important to do it this way so we don't clean up the temp dir in a subprocesss
            _global['sandbox_dir_to_cleanup'] = os.environ['KACHERY_CLOUD_SANDBOX_DIR']
    else:
        # We turn off the sandbox, but if we turn it back on again, we want to use the same dir for this process
        os.environ['KACHERY_CLOUD_USE_SANDBOX'] = '0'

def get_kachery_cloud_dir(*, respect_sandbox: bool=True):
    from pathlib import Path
    if respect_sandbox and (os.getenv('KACHERY_CLOUD_USE_SANDBOX', '') == '1'):
        return os.environ['KACHERY_CLOUD_SANDBOX_DIR']
    homedir = str(Path.home())
    hsd = os.getenv('KACHERY_CLOUD_DIR', f'{homedir}/.kachery-cloud')
    if not os.path.exists(hsd):
        os.makedirs(hsd)
    return hsd

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))

# We use environ variables for this so that the info is passed on to subprocesses
if os.getenv('KACHERY_CLOUD_SANDBOX_DIR', None) is None:
    # We don't actually mkdir until it is used
    # I found that electron remaps the /tmp directory, so we can't use /tmp. Probably just as well.
    os.environ['KACHERY_CLOUD_SANDBOX_DIR'] = f'{get_kachery_cloud_dir()}/sandbox/{_random_string(8)}'
if os.getenv('KACHERY_CLOUD_USE_SANDBOX', None) is None:
    os.environ['KACHERY_CLOUD_USE_SANDBOX'] = '0'

_global = {'sandbox_dir_to_cleanup': None}

def at_exit():
    # important to do it this way so we don't clean up the temp dir in a subprocesss
    sandbox_dir_to_cleanup = _global['sandbox_dir_to_cleanup']
    if sandbox_dir_to_cleanup is not None:
        if os.path.exists(sandbox_dir_to_cleanup):
            print(f'Cleaning up sandbox dir: {sandbox_dir_to_cleanup}')
            shutil.rmtree(sandbox_dir_to_cleanup)

atexit.register(at_exit)