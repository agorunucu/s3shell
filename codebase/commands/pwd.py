import global_vars


def dispatch(params):
    path = "/"
    if global_vars.current_bucket is not None:
        path += global_vars.current_bucket
        if global_vars.current_dir is not None:
            path += '/' + global_vars.current_dir
    print(path)
    if path != '/':
        print(f"s3:/{path}/")
