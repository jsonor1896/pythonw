import random
import requests


def ip2long(ip):
    ipnum = 0
    iplist = ip.split('.')
    for i in range(4):
        ipnum = ipnum + int(iplist[i]) * 256 ** (3 - i)

    return ipnum


def long2ip(ipnum):
    iplist = []

    for i in range(4):
        iplist.append(ipnum % 256)
        ipnum = ipnum // 256

    ip = ''
    for i in range(4):
        ip += str(iplist[3 - i])
        if i == 3:
            break
        ip += '.'

    return ip


def maskToIpNum(ip):
    ips = ip.split('/')
    count = int(ips[1])
    ipstr = ips[0]

    ipnum = ip2long(ipstr)
    mask = 0
    for i in range(count):
        mask = mask | (0x01 << (31 - i))

    startip = ipnum & mask
    endip = startip + 2 ** (32 - count)
    print(long2ip(startip))
    print(long2ip(endip))

"""
192.168.1.1/24
192.168.1.1/25
"""

if __name__ == '__main__':
    maskToIpNum('192.168.1.1/32')




