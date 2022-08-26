import kachery_cloud as kcl

kcl.use_sandbox()
uri = kcl.store_text_local('abcdefghi')
print(uri)
print(kcl.load_text(uri))
kcl.use_sandbox(False)
uri = kcl.store_text_local('abcdefghij')
print(uri)
print(kcl.load_text(uri))
raise Exception('test')