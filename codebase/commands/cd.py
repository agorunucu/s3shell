import global_vars
import sys
from helper.path_helper import get_absolute_path, check_if_path_exists, calculate_relativity


def dispatch(params):
    if not check_input(params):
        return

    if len(params) == 0:
        params.append("/")

    if str(params[0]).strip() == '':
        params[0] += "/"

    stripped_path = str(params[0]).strip()

    if not stripped_path.startswith("/"):
        absolute_path = get_absolute_path(stripped_path)
    else:
        absolute_path = stripped_path

    calculated_absolute_path = calculate_relativity(absolute_path)
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

    is_exists, maybe_exception = check_if_path_exists(new_bucket, key=new_dir)
    if is_exists:
        global_vars.current_bucket = new_bucket
        if new_dir == "":
            global_vars.current_dir = None
        else:
            global_vars.current_dir = new_dir
    else:
        if maybe_exception is not None and "Access Denied" in str(maybe_exception):
            print("You don't have permission to access it.", file=sys.stderr)
        else:
            print("There is no dir as entered.")
        if new_dir == "":
            print(f"S3Version: s3://{new_bucket}/", file=sys.stderr)
        else:
            print(f"S3Version: s3://{new_bucket}/{new_dir}/", file=sys.stderr)
