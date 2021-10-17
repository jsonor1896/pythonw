import os
import threading

from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import sr1


class IcmpMtuAsync:

    def __init__(self):
        self.mtu = -1
        self.mtuList = []

    def calcOs(self, mtu):
        response = os.system(f'ping www.baidu.com -f -l {mtu} -n 1 -w 3000 > NUL')
        if response != 0: return
        if mtu > self.mtu:
            self.mtu = mtu

    def run(self, os=True):
        func = self.calcOs if os else self.calcScapy
        threads = []
        for mtu in range(1400, 1600):
            thread = threading.Thread(target=func, args=(mtu,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def calcScapy(self, mtu):
        payload = b'p' * mtu
        pkt = IP(dst='www.baidu.com', flags='DF') / ICMP() / payload
        answer = sr1(pkt, timeout=2, verbose=False)
        if answer and answer[ICMP].code == 0 and answer[ICMP].type == 0:
            if self.mtu < mtu:
                self.mtu = mtu
            self.mtuList.append(mtu)

if __name__ == '__main__':
    mtuTest = IcmpMtuAsync()
    mtuTest.run(os=False)
    print(mtuTest.mtu)
    print(max(mtuTest.mtuList))