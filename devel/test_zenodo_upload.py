import kachery_cloud as kcl


def main():
    uploader = kcl.initiate_zenodo_upload(
        author="Jeremy Magland",
        affiliation="Flatiron Institute",
        title="test kachery zenodo upload",
        description="test kachery zenodo upload",
        sandbox=True
    )
    uri1 = uploader.upload_file(kcl.store_json_local({'test-kachery-zenodo-upload': 1}), name='test-kachery-zenodo-upload-1.json')
    uri2 = uploader.upload_file(kcl.store_json_local({'test-kachery-zenodo-upload': 2}), name='test-kachery-zenodo-upload-2.json')
    uri3 = uploader.upload_file(kcl.store_json_local({'test-kachery-zenodo-upload': 3}), name='test-kachery-zenodo-upload-3.json')

    print(uri1)
    print(uri2)
    print(uri3)

    uploader.finalize_upload()

if __name__ == '__main__':
    main()