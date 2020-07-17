import hashlib


def get_hash_name(raw_data):
    '''The hashing function. raw_data is file content'''
    return hashlib.sha256(raw_data).hexdigest()


def custom_upload_path(instance, filename):
    '''Forms the path for file based on hash_name parametr'''
    hash_name = instance.hash_name
    dirname = hash_name[:2]
    return '{}/{}'.format(dirname, hash_name)