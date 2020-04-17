import global_vars
from botocore.exceptions import ProfileNotFound
from helper import cmd_helper, env_var_helper


def dispatch(params):
    if not check_input(params):
        return
    try:
        __change_profile(params[0])
    except ProfileNotFound:
        print(f"Profile [{params[0]}] is not found!")


def check_input(params):
    if len(params) != 1:
        print(f"'su' command takes one parameter; the profile name you want to switch. [Entered: {' '.join(params)}]")
        return False
    return True


def __change_profile(new_profile):
    global_vars.s3cli = cmd_helper.__generate_boto3_with_profile(new_profile)
    global_vars.current_profile = new_profile
    env_var_helper.init_environment_variables()
