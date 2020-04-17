import global_vars


def dispatch(params):
    for variable, value in global_vars.environment_variables.items():
        print(f"{variable}={value}")
