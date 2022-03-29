import os

def get_kachery_cloud_dir():
    from pathlib import Path
    homedir = str(Path.home())
    hsd = os.getenv('KACHERY_CLOUD_DIR', f'{homedir}/.kachery-cloud')
    if not os.path.exists(hsd):
        os.makedirs(hsd)
    return hsd