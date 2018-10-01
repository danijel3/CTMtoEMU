from pathlib import Path
from subprocess import Popen, PIPE, STDOUT


def sendCommands(commands):
    p = Popen(['R', '--vanilla'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    p.stdin.write(commands.encode('utf-8'))
    p.stdin.close()
    for l in p.stdout.readlines():
        pass


def compute(filepath: Path, cmds):
    dirpath = filepath.parent
    if len(cmds) == 0:
        return
    cmd_str = 'library("wrassp")\n'
    for cmd in cmds:
        cmd_str += f'{cmd}("{filepath.absolute()}",outputDirectory="{dirpath.absolute()}")\n'
    sendCommands(cmd_str)
