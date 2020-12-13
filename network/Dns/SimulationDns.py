from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP
from scapy.packet import ls
from scapy.sendrecv import sr1


class SimulationDns:

    """
    概念
        递归查询
        根域名
        顶级域名 net/com/cn
        权限域名 baidu.com
        子域名   app.baidu.com

        1 ------------ 15 16 ------------ 31
         Transaction ID
    """

    pass

if __name__ == '__main__':
    packet = IP(dst='114.114.114.114') / UDP(dport=53) / \
             DNS(id=168, opcode='QUERY', rd=1, qd=DNSQR(qname='www.baidu.com'))
    ans = sr1(packet)
    ls(ans)
    dns_ip = ans[DNS].an[1].rdata
    print(dns_ip)