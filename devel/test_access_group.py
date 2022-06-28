import kachery_cloud as kcl

access_group = 'kddvtdrlrl'
uri = kcl.store_text('some-text '*3, label='some_text.txt')
uri_enc = kcl.encrypt_uri(uri, access_group=access_group)

print(uri)
print(uri_enc)

txt2 = kcl.load_text(uri_enc)
print(txt2)