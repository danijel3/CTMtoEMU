import os
from subprocess import Popen, PIPE, STDOUT


def sendCommands(commands):
    with open(os.devnull, 'w') as n:
        p = Popen(['R', '--vanilla'], stdin=PIPE, stdout=n, stderr=STDOUT)
        p.stdin.write(commands)
        p.stdin.close()
        # for l in p.stdout.readlines():
        #     print l


def compute(filepath, cmds):
    if len(cmds) == 0:
        return
    cmd_str = 'library("wrassp")\n'
    for cmd in cmds:
        cmd_str += '{}("{}")\n'.format(cmd, filepath)
    sendCommands(cmd_str)
