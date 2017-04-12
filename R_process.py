import os
from subprocess import Popen, PIPE, STDOUT


def sendCommands(commands):
    with open(os.devnull,'w') as n:
        p = Popen(['R', '--vanilla'], stdin=PIPE, stdout=n, stderr=STDOUT)
        p.stdin.write(commands)
        p.stdin.close()


def computeFormants(filepath):
    commands = 'library("wrassp")\nforest("{}")\n'.format(filepath)
    sendCommands(commands)
