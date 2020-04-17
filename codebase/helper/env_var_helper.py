import global_vars
import os
import yaml
from pathlib import Path


def __get_default_environment_variables():
    return {
        # Add required environment variables here.
        # It may be overwritten if the environment file contains it.
    }


def __get_user_environment_variables_from_file(profile):
    current_file_path = Path(os.path.dirname(os.path.realpath(__file__)))
    env_file_path = current_file_path.parent.joinpath("environments").joinpath(f"{profile}.yaml")

    if os.path.exists(env_file_path):
        return yaml.safe_load(open(env_file_path))
    else:
        return {}


def init_environment_variables():
    profile = global_vars.current_profile
    environment_variables = __get_default_environment_variables()

    if profile is not None:
        profile_environment_variables = __get_user_environment_variables_from_file(profile)
        environment_variables = {**environment_variables, **profile_environment_variables}

    global_vars.environment_variables = environment_variables


def get_variable(variable, default=None):
    if variable in global_vars.environment_variables:
        return global_vars.environment_variables.get(variable)
    else:
        return default


def set_variable(variable, value):
    global_vars.environment_variables[variable] = value
    # Storing new value to the file is not currently supported.
    # profile = global_vars.current_profile
    # if profile is not None:
    #     __save_current_user_environment_variables_to_file(profile)


# def __save_current_user_environment_variables_to_file(profile):
#     current_file_path = Path(os.path.dirname(os.path.realpath(__file__)))
#     env_file_path = current_file_path.parent.joinpath("environments").joinpath(f"{profile}.yaml")
#
#     with open(env_file_path, 'w') as outfile:
#         yaml.dump(global_vars.environment_variables, outfile, default_flow_style=False)
