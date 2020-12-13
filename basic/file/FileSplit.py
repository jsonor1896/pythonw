import os


class FileSplit:

    def __init__(self, file, dst_dir):
        """
        构造文件分割类
        :param file: 文件名字
        :param dst_dir: 分解后的文件目标目录
        """
        self.__file = file
        self.__dst_dir = dst_dir

        if not os.path.exists(self.__dst_dir):
            os.mkdir(self.__dst_dir)

    def do(self, count):
        """
        分割文件
        :param count: 分割数量
        """

        buf = self.__read_file_buffer()
        size = int(len(buf) / count) + 1

        for i in range(0, count):
            name = self.__get_dst_full_file_name(i)
            if i == 0:
                name += os.path.splitext(self.__file)[1]
            self.write(name, buf[i * size: (i + 1) * size])

    def do2(self, count):
        """
        分割文件，给分割好的每个文件前添加一个顺序表示：
        第一个文件，添加字节0x01
        第二个文件，添加字节0x02
        :param count: 分割数量
        """
        buf = self.__read_file_buffer()
        size = int(len(buf) / count) + 1

        for i in range(0, count):
            name = self.__get_dst_full_file_name(str(i))
            bs = buf[i * size:(i + 1) * size]
            self.write(name, bytearray([i]), bs)

    def __read_file_buffer(self):
        """
        读取需要分割的文件二进制数值（仅限于小文件）
        :return: 文件的bytes对象
        """
        with open(self.__file, 'rb') as f:
            buffer = f.read()

            return buffer

    def __get_dst_full_file_name(self, name):
        """
        获取文件的全路径名称
        :param name: 文件名称
        :return: 文件的全路径名称
        """
        return self.__dst_dir + '/' + str(name)

    @classmethod
    def write(cls, file_name, *buffer):
        """
        将字节序列写入到指定的文件中
        :param file_name: 文件名字（全路径）
        :param buffer: 字节序列
        """
        with open(file_name, 'wb') as f:
            for bf in buffer:
                f.write(bf)


class Combination:

    @classmethod
    def do(cls, directory, dst_name):
        """
        文件组合
        :param directory: 文件目录
        :param dst_name: 文件名称
        """
        fragments = [directory + '/' + name for name in os.listdir(directory)]
        fragment_count = len(fragments)
        current_index = 0
        with open(dst_name, 'wb') as f:
            for count in range(0, fragment_count):
                for frag in fragments:
                    index, buf = cls.read(frag)
                    if index == current_index:
                        f.write(buf)
                        current_index += 1
                        fragments.remove(frag)
                        continue

    @classmethod
    def read(cls, file):
        with open(file, 'rb') as f:
            index = f.read(1)
            buf = f.read()

            return index[0], buf


if __name__ == '__main__':
    # fs = FileSplit('../material/QmXh6p3DGKfvEVwdvtbiH7SPsmLDfL7LXrowAZtQjkjw73.jpg', 'img')
    # fs.do2(2)
    Combination.do('./img', '2.jpg')
