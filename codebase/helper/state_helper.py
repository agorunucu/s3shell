import global_vars


def get_current_state():

    return f"[{global_vars.current_profile}] {__get_current_dir()}"


def __get_current_dir():
    current_bucket = global_vars.current_bucket
    current_dir = global_vars.current_dir

    if current_bucket is None:
        return "/"

    if current_dir is None:
        return f"{current_bucket}"

    if str(current_dir).endswith("/"):
        current_dir = current_dir[:-1]

    return current_dir.split('/')[-1]
