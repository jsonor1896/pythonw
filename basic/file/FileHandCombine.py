import os


class FileHandCombine:

    def __init__(self, files_path):
        """
        文件手动拼接方式
        :param files_path: 文件路径集合
        """
        self.__files_path = files_path

    def combine(self, sure_num, ext, directory):
        """
        对文件列表中的文件进行拼接操作，但前sure_num项不参加拼接
        :param sure_num: 已经完成拼接的个数
        :param ext: 文件的扩展名
        :param directory: 文件目录
        """

        # 写入已经拼接好的前半部分的图片信息
        head = self.read_binary(self.__files_path[0:sure_num])

        for file in self.__files_path[sure_num:]:
            name = '{}/{}.{}'.format(directory,
                                     os.path.basename(file).split('.')[0],
                                     ext)
            with open(name, 'wb') as wr:
                wr.write(head)
                buf = self.read_binary([file])
                wr.write(buf)

    @classmethod
    def read_binary(cls, files):
        """
        读取指定文件，返回二进制序列
        :param files: 文件路径集合
        :return: 字节数组
        """
        bs = bytes()
        for file in files:
            with open(file, 'rb') as rd_handler:
                bs += rd_handler.read()

        return bs


if __name__ == '__main__':
    images = ['..\.\material\QmXh6p3DGKfvEVwdvtbiH7SPsmLDfL7LXrowAZtQjkjw73.jpg',
              '..\.\material\QmZkF524d8HWfF8k2yLrZwFz9PtaYgCwy3UqJP5Ahk5aXH',
              '..\.\material\QmU59LjvcC1ueMdLVFve8je6vBY48vkEYDQZFiAbpgX9mf',
              '..\.\material\Qme7fkoP2scbqRPaVv6JEiaMjcPZ58NYMnUxKAvb2paey2',
              '..\.\material\QmfUbHZQ95XKu9vd5XCerhKPsogRdYHkwx8mVFh5pwfNzE',
              '..\.\material\QmXFSNiJ8BdbUKPAsu3oueziyYqeYhi3iyQPXgVSvqTBtN']

    combine = FileHandCombine(images)
    combine.combine(5, 'jpg', '.././img')
