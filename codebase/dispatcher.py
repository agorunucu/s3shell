from commands import ls, cd, exit, pwd

dispatcher = {
    'ls': ls.dispatch,
    'cd': cd.dispatch,
    'exit': exit.dispatch,
    'pwd': pwd.dispatch
}
