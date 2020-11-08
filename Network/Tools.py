import sys
from configparser import ConfigParser

from scapy.arch import *
from scapy.layers.inet import *
from scapy.layers.l2 import *


class Tools:
    Ether_BoardCast = 'FF:FF:FF:FF:FF:FF'
    Ether_Empty = '00:00:00:00:00:00'

    @staticmethod
    def get_property(property_name, config_file_name='config.ini'):
        """
        获取配置文件中的属性值
        :param property_name: 属性名称
        :param config_file_name: 配置文件名称
        :return: 属性信息
        """
        parser = ConfigParser()
        parser.read(config_file_name)

        return parser.get('debug', property_name)

    @staticmethod
    def get_network_info(ether_name=None):
        """
        获取指定网卡的mac地址以及ip地址信息
        :param ether_name: 网卡名字
        :return: (mac, ip)
        """
        mac = None
        ip4 = None

        if ether_name:
            if "win32" in sys.platform:
                windows_if_list = get_windows_if_list()
                for ether in windows_if_list:
                    if ether['name'] == ether_name:
                        mac, ip4 = ether['mac'], ether['ips'][1]
                        break
            else:
                mac, ip4 = get_if_hwaddr(ether_name), get_if_addr(ether_name)

            if mac is None or ip4 is None:
                raise Exception('read ethernet information failed!')
        else:
            ip4 = IP(dst='www.baidu.com').src
            mac = Ether().src

        return mac, ip4

    @staticmethod
    def get_random_port():
        return random.randint(3000, 65534)

    @staticmethod
    def get_random_ip():
        return '.'.join([str(random.randint(1, 254)) for _ in range(0, 4)])

    @staticmethod
    def random_bytes_message(size=32):
        bytes_available = (
            b'abcdefghijklmnopqrstuvwxyz'
            b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            b'1234567890'
        )

        message = [
            random.choice(bytes_available)
            for _ in range(size)
        ]

        return bytes(message)
