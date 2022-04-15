from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[
        'bin/kachery-cloud',
        'bin/kachery-cloud-store',
        'bin/kachery-cloud-load',
        'bin/kachery-cloud-init',
        'bin/kachery-cloud-cat'
    ],
    include_package_data = True,
    install_requires=[
        'requests',
        'click',
        'simplejson',
        'cryptography',
        'pubnub',
        'dask[distributed]'
    ]
)
