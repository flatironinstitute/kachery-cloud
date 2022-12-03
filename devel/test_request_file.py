import kachery_cloud as kcl

uri = kcl.store_text_local('2022.12.2.r8')
result = kcl.request_file(uri, resource='test1', timeout_sec=5, ignore_local=True)
print(result)