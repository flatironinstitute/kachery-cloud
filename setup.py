from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[
        'bin/kachery-cloud',
        'bin/kachery-cloud-store',
        'bin/kachery-cloud-link',
        'bin/kachery-cloud-load',
        'bin/kachery-cloud-load-info',
        'bin/kachery-cloud-init',
        'bin/kachery-cloud-cat',
        'bin/kachery-cloud-store-local',
        'bin/kachery-cloud-share-local-files-experimental',
        'bin/kachery-cloud-request-file-experimental'
    ],
    include_package_data = True,
    install_requires=[
        'requests',
        'click',
        'simplejson',
        'cryptography',
        'pubnub==6.3.*', # There is a bug in 6.4.0
        'dask[distributed]'
    ]
)
