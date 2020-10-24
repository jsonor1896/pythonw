import nmap

class IcmpNmap:

    @staticmethod
    def start(ips):
        scanner = nmap.PortScanner()
        root = scanner.scan(ips, arguments='-sn -PE')

        scanstats = root['nmap']['scanstats']
        result = {
            'scan_stats': {
                'up': scanstats['uphosts'],
                'down': scanstats['downhosts'],
                'total': scanstats['totalhosts']
            }
        }

        scan = root['scan']
        host = {}
        for key, value in scan.items():
            ip = IcmpNmap.get_default_none(value['addresses'], 'ipv4')
            mac = IcmpNmap.get_default_none(value['addresses'], 'mac')
            vendor = IcmpNmap.get_default_none(value['vendor'], mac)
            reason = IcmpNmap.get_default_none(value['status'], 'reason')
            host[ip] = {
                'mac': mac,
                'vendor': vendor,
                'reason': reason
            }

        result['host'] = host
        return result

    @staticmethod
    def get_default_none(dictionary, key):
        return dictionary[key] if key in dictionary else None


if __name__ == '__main__':
    result = IcmpNmap.start('192.168.2.1/24')
    for key, value in result.items():
        if isinstance(value, dict):
            print(key)
            for key1, value1 in value.items():
                print(key1, value1)
        else:
            print(key, value)
