import winreg


def printNets():
    subKey = 'SOFTWARE\Microsoft\Windows NT\CurrentVersion\\NetworkList\Signatures\\Unmanaged'
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subKey)
    print('\n[*] Networks you have joined')
    count, _, _ = winreg.QueryInfoKey(key)

    for n in range(count):
        guid = winreg.EnumKey(key, n)
        netKey = winreg.OpenKey(key, str(guid))

        deviceName, _ = winreg.QueryValueEx(netKey, 'Description')
        mac, _ = winreg.QueryValueEx(netKey, 'DefaultGatewayMac')
        if mac:
            mac = ':'.join(['%02x' % ch for ch in mac])
        else:
            mac = ':'.join(['--' for _ in range(6)])

        print('{:<20}\t{}'.format(mac, deviceName))


if __name__ == '__main__':
    printNets()
