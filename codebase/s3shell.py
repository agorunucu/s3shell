#!/usr/bin/env python3
from helper import cmd_helper, env_var_helper, state_helper
import global_vars
from dispatcher import dispatcher
import sys


def main_loop():
    while True:
        try:
            user_input = input(f"{state_helper.get_current_state()}> ")
        except KeyboardInterrupt:
            print()  # put newline
            continue
        except EOFError:
            print()
            print("Exiting...")
            sys.exit(0)
        except Exception as e:
            print(e)
            print(f"Unexpected error occured. Please report this command to the developer.",
                  file=sys.stderr)
            continue

        if user_input == '':
            continue

        splitted_user_input = user_input.split(' ')
        user_command = dispatcher.get(splitted_user_input[0])
        if user_command is not None:
            user_command(splitted_user_input[1:])
        else:
            print(f"Command '{splitted_user_input[0]}' not found.")


if __name__ == "__main__":
    parser, args = cmd_helper.parse()
    global_vars.s3cli = cmd_helper.init_s3cli(parser, args)
    env_var_helper.init_environment_variables()
    main_loop()
