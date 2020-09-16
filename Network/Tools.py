import sys
from configparser import ConfigParser

from scapy.arch import *


class Tools:

    Ether_BoardCast = 'FF:FF:FF:FF:FF:FF'
    Ether_Empty = '00:00:00:00:00:00'

    @staticmethod
    def get_property(property_name, config_file_name='config.ini'):
        parser = ConfigParser()
        parser.read(config_file_name)

        return parser.get('debug', property_name)


    @staticmethod
    def get_network_info(ether_name):
        """
        获取指定网卡的mac地址以及ip地址信息
        :param ether_name: 网卡名字
        :return: (mac, ip)
        """

        mac = None
        ip4 = None

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

        return mac, ip4
