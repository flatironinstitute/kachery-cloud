import kachery_cloud as kcl


def main():
    kcl.set_mutable('@abc/def', 'ghi')
    a = kcl.get_mutable('@abc/def')
    print(a)
    kcl.delete_mutable('@abc/def')
    a = kcl.get_mutable('@abc/def')
    print(a)

if __name__ == '__main__':
    main()