from argparse import ArgumentParser

import pexpect
from pexpect import pxssh


class SSH:
    PROMPT_TXT = ['# ', '>>> ', '> ', '\$ ']

    def __init__(self, user, password, host):
        """
        ssh连接

        :param user: 用户名
        :param password: 密码
        :param host: 连接主机
        """

        self.user = user
        self.host = host
        self.password = password
        self.cmd = 'ssh {user}@{host}'.format(user=self.user, host=self.host)

    def connect(self, command='cat /etc/shadow | grep root'):
        """
        使用pexpect进行交互式的连接

        :param command: 连接完成之后，执行命令进行测试
        :return 返回command命令执行的结果
        """

        sub = pexpect.spawn(self.cmd)
        ret = sub.expect(['Are you sure you want to continue connecting',
                          '[P|p]assword', '[L|l]ogin'], timeout=20)

        # 第一次认证
        if ret == 0:
            self.do_authorization(sub)
            self.do_password(sub)

        if ret == 2:
            self.do_password(sub)

        return self.do_login(sub, command)

    def do_authorization(self, sub):
        """
        处理认证

        :param sub: 子进程
        """
        sub.sendline('yes')
        sub.expect('[P|p]assword', timeout=20)

    def do_password(self, sub):
        """
        处理密码返回

        :param sub: 子进程
        """
        sub.sendline(self.password)
        sub.expect(self.PROMPT_TXT, timeout=10)

    def do_login(self, sub, command):
        """
        处理登录后命令的发送

        :param sub: 子进程
        :param command: 发送的命令
        """
        sub.expect(self.PROMPT_TXT)
        sub.sendline(command)
        sub.expect(self.PROMPT_TXT)

        return str(sub.before, encoding='utf-8')

    def connect_ex(self, comand='cat /etc/shadow | grep root'):
        """
        使用pxssh库进行连接

        :param comand: ssh连接成功后发送的命令
        """

        ssh = pxssh.pxssh()
        ssh.login(self.host, self.user, self.password)
        ssh.sendline(comand)
        ssh.prompt(timeout=20)

        return ssh.before

if __name__ == '__main__':
    parser = ArgumentParser(description='ssh connected testing')

    parser.add_argument('-u', '--user', default='root', type=str)
    parser.add_argument('-w', '--password', default='root', type=str)
    parser.add_argument('-p', '--host', required=True, type=str)

    args = parser.parse_args()

    user = args.user
    host = args.host
    password = args.password

    sh = SSH(user, password, host)
    # sh.connect()
    sh.connect_ex()
