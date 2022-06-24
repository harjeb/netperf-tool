from invoke import Responder
import invoke
from invoke import run
import logging
import time
import os


def cmd(command):
    try:
        f = run(command,pty=False)
        return f.ok,f.stdout+f.stderr
    except invoke.exceptions.UnexpectedExit as e:
        logging.error('命令错误 %s' % e)
        # 命令错误也会返回错误信息
        return False,e.result.stdout+e.result.stderr
