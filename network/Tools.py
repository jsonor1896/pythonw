from configparser import ConfigParser

from scapy.layers.inet import *


class Tools:

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
