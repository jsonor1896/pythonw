import random

from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr


class TcpScapy:

    pass


if __name__ == '__main__':
    pk = IP(dst='10.10.95.247') / TCP(sport=10901, dport=10001, seq=random.randint(1000, 65534), flags='S')
    ans, unans = sr(pk, timeout=2, verbose=False)
    if ans:
        print('answer')
        ans[0][1].show()
    if unans:
        print('unanswer')
        unans.show()