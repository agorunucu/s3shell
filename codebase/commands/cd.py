import global_vars
import sys


def dispatch(params):
    if not check_input(params):
        return

    if len(params) == 0:
        params.append("/")

    if str(params[0]).strip() == '':
        params[0] += "/"

    stripped_path = str(params[0]).strip()

    if not stripped_path.startswith("/"):
        absolute_path = __get_absolute_path(stripped_path)
    else:
        absolute_path = stripped_path

    calculated_absolute_path = __calculate_relativity(absolute_path)
    __go_absolute_path(calculated_absolute_path)


def check_input(params):
    if len(params) > 1:
        print(f"'cd' command takes at most one parameter. [Entered: {' '.join(params)}]")
        return False
    return True


def __go_absolute_path(absolute_path):
    if absolute_path == '/':
        global_vars.current_bucket = None
        global_vars.current_dir = None
        return

    if absolute_path.endswith('/'):
        absolute_path = absolute_path[:-1]

    splitted_path = str(absolute_path).split("/")
    new_bucket = splitted_path[1]
    if len(splitted_path) > 2:
        new_dir = "/".join(splitted_path[2:])
    else:
        new_dir = ""

    if __check_if_path_exists(new_bucket, new_dir):
        global_vars.current_bucket = new_bucket
        if new_dir == "":
            global_vars.current_dir = None
        else:
            global_vars.current_dir = new_dir
    else:
        print("Whether there is no dir or you don't have permission to access it.", file=sys.stderr)
        if new_dir == "":
            print(f"S3Version: s3://{new_bucket}/", file=sys.stderr)
        else:
            print(f"S3Version: s3://{new_bucket}/{new_dir}/", file=sys.stderr)


def __get_absolute_path(relative_path):
    if global_vars.current_bucket is None:
        absolute_path = '/' + relative_path
    elif global_vars.current_dir is None:
        absolute_path = '/' + global_vars.current_bucket + '/' + relative_path
    else:
        absolute_path = '/' + global_vars.current_bucket + '/' + global_vars.current_dir + '/' + relative_path
    return absolute_path


def __check_if_path_exists(bucket, key=""):
    s3cli = global_vars.s3cli
    try:
        if key is "":
            s3cli.head_bucket(Bucket=bucket)
            return True
        else:
            if not key.endswith("/"):
                key += "/"
            response = s3cli.list_objects_v2(
                Bucket=bucket,
                MaxKeys=1,
                Prefix=key
            )
            return int(response['KeyCount']) > 0
    except Exception as e:
        print(e)
        return False


def __calculate_relativity(relative_path):
    splitted_path = relative_path.split('/')

    while True:
        is_there_any_change = False
        for index, name in enumerate(splitted_path):
            if name == "..":
                # Simulate /..
                if index == 1:
                    del splitted_path[index]
                else:
                    del splitted_path[index]
                    del splitted_path[index - 1]
                is_there_any_change = True
                break
        if not is_there_any_change:
            break

    result = "/".join(splitted_path)
    if not result.startswith('/'):
        result = '/' + result

    return result
