import kachery_cloud as kcl

###############################################
kcl.use_sandbox()

uri = kcl.store_text_local('abcdefghi')
print(uri)
print(kcl.load_text(uri))

# test that cloud upload still works
uri = kcl.store_text('test-sandbox')
print(uri)

###############################################
kcl.use_sandbox(False)

uri = kcl.store_text_local('abcdefghij')
print(uri)
print(kcl.load_text(uri))