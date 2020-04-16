#!/usr/bin/env python3
from initial import cmd_parser
import state_helper
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
    parser, args = cmd_parser.parse()
    global_vars.s3cli = cmd_parser.init_s3cli(parser, args)
    main_loop()
