import threading
import time

from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import sniff, send, sr1

HostLists = set()
MonitorTime = time.time()
SendFinished = False


def sniffCallback(packet):
    if packet and packet.haslayer(IP) and \
            packet.haslayer(ICMP) and packet[ICMP].code == 0 and packet[ICMP].type == 0:
        HostLists.add(packet[IP].src)


def stopFilterCallback(packet):
    global MonitorTime, SendFinished
    interval = time.time() - MonitorTime
    if SendFinished and interval > 5:
        return True


def sendAll(prefixIp):
    time.sleep(2)
    threads = []
    for i in range(1, 254):
        ip = f'{prefixIp}.{i}'
        t1 = threading.Thread(target=sending, args=(ip,))
        t1.start()
        threads.append(t1)

    for t1 in threads:
        t1.join()

    global MonitorTime, SendFinished
    MonitorTime = time.time()
    SendFinished = True


def sending(host):
    pkt = IP(dst=host) / ICMP()
    print('start to send packet to {}\n'.format(host), end='')
    send(pkt, verbose=False, iface='Realtek PCIe GbE Family Controller')


if __name__ == '__main__':
    thread = threading.Thread(target=sendAll, args=('10.30.80',))
    thread.start()
    sniff(prn=sniffCallback, stop_filter=stopFilterCallback, iface='Realtek PCIe GbE Family Controller')

    for item in sorted(HostLists):
        print(item)

    print(len(HostLists))
