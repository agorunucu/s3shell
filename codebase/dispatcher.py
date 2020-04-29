from commands import ls, cd, exit, pwd, printenv, su, who, mkdir

dispatcher = {
    'ls': ls.dispatch,
    'cd': cd.dispatch,
    'exit': exit.dispatch,
    'pwd': pwd.dispatch,
    'printenv': printenv.dispatch,
    'su': su.dispatch,
    'who': who.dispatch,
    'mkdir': mkdir.dispatch
}
