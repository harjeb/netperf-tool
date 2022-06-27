import subprocess

def cmd(command):
    try:
        f = subprocess.getoutput(command)
        return f
    except Exception as e:
        print('命令错误 %s' % e)
        # 命令错误也会返回错误信息
        return False
