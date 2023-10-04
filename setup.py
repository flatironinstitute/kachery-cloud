from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    include_package_data = True,
    install_requires=[
        'requests',
        'click',
        'simplejson',
        'cryptography',
        'pubnub>=7.2.0', # There is a bug in 6.4.0
        'dask[distributed]'
    ],
    entry_points={
        'console_scripts': [
            'kachery-cloud = kachery_cloud.cli:cli',
            'kachery-cloud-store = kachery_cloud.cli:store_file',
            'kachery-cloud-link = kachery_cloud.cli:link_file',
            'kachery-cloud-load = kachery_cloud.cli:load_file',
            'kachery-cloud-load-info = kachery_cloud.cli:load_file_info',
            'kachery-cloud-init = kachery_cloud.cli:init',
            'kachery-cloud-cat = kachery_cloud.cli:cat_file',
            'kachery-cloud-store-local = kachery_cloud.cli:store_file_local',
            'kachery-cloud-share-local-files-experimental = kachery_cloud.cli:share_local_files_experimental',
            'kachery-cloud-request-file-experimental = kachery_cloud.cli:request_file_experimental',
            'kachery-cloud-admin-delete-file = kachery_cloud.cli:admin_delete_file'
        ]
    }
)
