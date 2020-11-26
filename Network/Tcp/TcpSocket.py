import concurrent
import os
import socket
from argparse import ArgumentParser
from concurrent.futures.process import ProcessPoolExecutor


class TcpSocket:

    def __init__(self, host, ports):
        """
        Tcp Socket对象

        :param host: 目标ip地址
        :param ports: 端口列表
        """
        self.host = host
        try:
            self.ip4 = socket.gethostbyname(host)
        except:
            print('[-] 无法解析主机地址', host)

        self.ports = ports

    def checkport(self, port, detail=False):
        """
        以全TCP连接三次握手的方式进行指定端口的扫描

        :param port: 端口
        :param detail: 是否获取端口的应用标识
        """
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

        # connect和connect_ex的区别
        # https://docs.python.org/3/library/socket.html
        code = skt.connect_ex((self.ip4, port))
        if code == 0:
            txt = f'[+] {port} tcp open'
            if detail:
                skt.send('port detial information\r\n'.encode('utf-8'))
                response = skt.recv(100)
                txt += f'\t[+] {str(response)}'
        else:
            txt = f'[-] {port} tcp closed'

        skt.close()
        print(txt)

    def scan(self, detail=False):
        """
        以全TCP连接三次握手的方式进行全端口的扫描

        :param detail: 是否获取端口的应用标识
        """

        socket.setdefaulttimeout(1)
        for port in self.ports:
            self.checkport(port, detail)

    def async_scan(self, detial=False):
        """
        使用异步的方式进行TCP连接三次握手的方式进行全端口的扫描

        :param detial: 是否输出详情
        """
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            tasks = [executor.submit(self.checkport, port, detial) for port in self.ports]
            concurrent.futures.wait(tasks, return_when=concurrent.futures.ALL_COMPLETED)


if __name__ == '__main__':
    parser = ArgumentParser(description='tcp port scan')
    parser.add_argument('-t', '--host', required=True, type=str)
    parser.add_argument('-p', '--ports', required=True, type=str)
    parser.add_argument('-d', '--detail', action='store_true', default=False)
    parser.add_argument('-a', '--thread', action='store_true', default=False)
    args = parser.parse_args()

    # port = 1-1000
    if '-' in args.ports:
        s = args.ports.split('-')
        ports = [port for port in range(int(s[0]), int(s[1]) + 1)]

    # port = 10,22,34,90
    elif ',' in args.ports:
        ports = [int(port) for port in args.ports.split(',')]

    # port = 10
    else:
        ports = int(args.ports)

    tcpSk = TcpSocket(args.host, ports)

    if args.thread:
        tcpSk.async_scan(args.detail)
    else:
        tcpSk.scan(args.detail)
