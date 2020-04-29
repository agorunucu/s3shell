import global_vars


def get_absolute_path(relative_path):
    """
    :param relative_path: the relative path which is not started with '/'
    :return: absolute path
    """
    if global_vars.current_bucket is None:
        absolute_path = '/' + relative_path
    elif global_vars.current_dir is None:
        absolute_path = '/' + global_vars.current_bucket + '/' + relative_path
    else:
        absolute_path = '/' + global_vars.current_bucket + '/' + global_vars.current_dir + '/' + relative_path
    return absolute_path


def check_if_path_exists(bucket, key=""):
    """
    Checks whether path exists or not
    :param bucket: Bucket name
    :param key: Object key, (the default is: "", empty string)
    :return: Boolean
    """
    s3cli = global_vars.s3cli
    try:
        if key is None or key is "":
            s3cli.head_bucket(Bucket=bucket)
            return True, None
        else:
            if not key.endswith("/"):
                key += "/"
            response = s3cli.list_objects_v2(
                Bucket=bucket,
                MaxKeys=1,
                Prefix=key
            )
            return int(response['KeyCount']) > 0, None
    except Exception as e:
        return False, e


def calculate_relativity(relative_path):
    """

    :param relative_path: which may contains relativity strings (. or ..)
    :return: the path that has been applied for all relativity strings
    """
    splitted_path = relative_path.split('/')

    while True:
        is_there_any_change = False
        for index, name in enumerate(splitted_path):
            if name == "..":
                # Simulate /..
                # Remove current dir
                del splitted_path[index]
                if index != 1:
                    # Remove upper dir if its currently not in root
                    del splitted_path[index - 1]
                is_there_any_change = True
                break
            elif name == ".":
                # Simulate /.
                # Remove current dir
                del splitted_path[index]
                is_there_any_change = True
                break
        if not is_there_any_change:
            break

    result = "/".join(splitted_path)
    if not result.startswith('/'):
        result = '/' + result

    return result


def get_bucket_key_from_absolute_path(absolute_path):
    """

    :return: (bucket_name, object_key)
    """
    if absolute_path is None:
        return None, None
    splitted_path = str(absolute_path).split('/')
    if len(splitted_path) == 2 and splitted_path[1] == '':
        return None, None
    if len(splitted_path) == 2:
        return splitted_path[1], None
    return splitted_path[1], '/'.join(splitted_path[2:])
