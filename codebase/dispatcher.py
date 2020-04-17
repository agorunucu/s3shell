from commands import ls, cd, exit, pwd, printenv

dispatcher = {
    'ls': ls.dispatch,
    'cd': cd.dispatch,
    'exit': exit.dispatch,
    'pwd': pwd.dispatch,
    'printenv': printenv.dispatch
}
