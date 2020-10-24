import concurrent
import socket
from concurrent.futures.process import ProcessPoolExecutor


class TcpSocket:

    def __init__(self, pdst):
        """
        Tcp Socket对象
        :param pdst: 目标ip地址
        """
        self.__pdst = pdst
        self.__sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    def port_state(self, port):
        """
        扫描主机的特定端口号，返回该端口的存活状态
        connect/connect_ex的区别：https://blog.51cto.com/yangrong/1339593
        :param port: 端口列表
        :return: 端口存活，返回True，否则返回False
        """
        return self.__sk.connect_ex((self.__sk, port))

    def port_scan(self, port_range):
        """
        扫描主机的一系列端口，返回端口的状态集合
        :param port_range: 端口集合
        :return: 端口的状态集合
        """
        res = []
        for port in port_range:
            state = self.port_state(port)
            res.append((port_range, state))

        return res

    def port_scan_async(self, port_range):
        """
        使用多核方式进行主机的端口扫描
        :param port_range: 端口范围
        :return: 端口的状态集合
        """
        res = []
        with ProcessPoolExecutor(max_workers=6) as executor:
            func_futures = [executor.submit(self.port_state, port) for port in port_range]
            for future in concurrent.futures.as_completed(func_futures):
                res.append(future.result())

        return res