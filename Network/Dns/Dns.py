import socket

from whois import whois


class Dns:

    @staticmethod
    def get_ip(domain_name:str):
        """
        通过socket.gethostbyname获取ip地址信息
        :param domain_name: 主机域名
        :return: ip地址信息
        """
        ip = socket.gethostbyname(domain_name)

        return ip

    @staticmethod
    def whois(domain_name:str):
        """
        通过python-whois包进行whois查询
        :param domain_name: 主机域名
        :return: whois信息查询结果
        """
        return whois(domain_name)
