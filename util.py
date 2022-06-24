from invoke import Responder
import invoke
from invoke import run
import paramiko
import socket
import logging
import time
from configobj import ConfigObj
from configparser import ConfigParser
import os


def not_empty(s):
    return s and s.strip()


class Eth(object):
    '''
    网卡操作
    c = SSH_Conn(host=hostip,usr=usrname,pw=password)
    alleth = Eth(c).eths
    '''
    def __init__(self):
        '''
        eths 为网卡和ip 字典
        '''
        f,self.temp = cmd("cat /proc/net/dev | awk '{i++; if(i>2){print $1}}' | sed 's/^[\t]*//g' | sed 's/[:]*$//g'")
        ethlist = filter(not_empty, self.temp.splitlines())
        self.eths = {}
        for i in ethlist:
            f,ip = cmd(("/usr/sbin/ifconfig %s|sed -n 2p|awk '{ print $2 }'|tr -d 'addr:'")% i)
            self.eths[i] = "".join(ip.split())
            

    def main_eth(self, hostip=None):
        '''返回主网卡名

        返回主网卡名（通过判断是否为远程ip）
        Eth(c).main_eth(‘172.0.0.1’)

        Args:
            hostip (str): 机器ip

        Returns:
            str: 网卡名

        '''
        for k in self.eths:
            if self.eths[k] == hostip:
                return k



class Dictionary(dict):
    """

    把settings.ini中的参数添加值dict

    """
    def __getattr__(self, keyname):
         #如果key值不存在则返回默认值"not find config keyname"
         return self.get(keyname, "settings.ini中没有找到对应的keyname")


class Conf(object):
    '''
    ConfigParser二次封装，在字典中获取value
    '''
    def __init__(self):
        # 设置conf.ini路径
        current_dir = os.path.dirname(__file__)
        top_one_dir = os.path.dirname(current_dir)
        file_name = top_one_dir + "/setting.ini"
        # 实例化ConfigParser对象
        self.config = ConfigParser()
        self.config.read(file_name)
        #根据section把key、value写入字典
        for section in self.config.sections():
            setattr(self, section, Dictionary())
            for keyname, value in self.config.items(section):
                setattr(getattr(self, section), keyname, value)

    def getconf(self, section):
        """配置文件读取

        读取ini文件
        用法：
        conf = Conf()
        info = conf.getconf("main").url

        Args:
            section (str): ini中的section名

        Returns:
            object: getattr()函数

        """
        if section in self.config.sections():
            pass
        else:
            logging.error("config.ini 找不到该 section")
        return getattr(self, section)



def modify_conf(info_list):
    """
    修改setting.ini配置
    """
    current_dir = os.path.dirname(__file__)
    top_one_dir = os.path.dirname(current_dir)
    file_name = top_one_dir + "/setting.ini"
    config = ConfigObj(file_name,encoding='UTF8')
    config['Infos']['server_ip'] = info_list[0]
    config['Infos']['server_usr'] = info_list[1]
    config['Infos']['server_pwd'] = info_list[2]
    config.write()



class Info(object):

    def __init__(self):
        self.server_ip = ''
        self.server_pwd = ''
        self.server_usr = ''
        self.update()

    def update(self):
        conf = Conf()
        self.server_usr = conf.getconf("Infos").server_usr
        self.server_pwd = conf.getconf("Infos").server_pwd
        self.server_ip = conf.getconf("Infos").server_ip



def cmd(command):
    try:
        f = run(command,pty=False)
        return f.ok,f.stdout+f.stderr
    except invoke.exceptions.UnexpectedExit as e:
        logging.error('命令错误 %s' % e)
        # 命令错误也会返回错误信息
        return False,e.result.stdout+e.result.stderr
