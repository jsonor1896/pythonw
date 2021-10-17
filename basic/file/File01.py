if __name__ == '__main__':
    file = open('D:\\1.gif', 'rb')
    print(file.read(1))
    print(file.seek(0))
    print(file.read(1))
