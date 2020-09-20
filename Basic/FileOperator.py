import itertools


class FileOperator:

    def __init__(self, file_path):
        self.__file_path = file_path


    def read_all_lines(self):
        with open(self.__file_path, 'r') as handler:
            txt = handler.readlines()
            return txt


    def read_lines(self):
        with open(self.__file_path, 'r') as handler:
            while True:
                txt = handler.readline()
                if len(txt) == 0: break
                yield txt


    def read_byte(self):
        with open(self.__file_path, 'rb') as handler:
            array_bytes = handler.read()
            return array_bytes


    def write_new(self, content):
        with open(self.__file_path, 'w') as handler:
            handler.write(content)


    def write_arrays(self, array):
        with open(self.__file_path, 'w') as handler:
            for item in array:
                handler.write(item)


class ImageCombination:

    def __init__(self, image_header, image_fragments):
        """
        将零散的图片信息组合成一张图片
        :param image_header: 起始图片
        :param image_fragments: 图片碎片
        """
        self.__image_fragments = image_fragments
        self.__image_header = image_header


    def combine(self):
        permuation = itertools.permutations(self.__image_fragments, len(self.__image_fragments))
        image_list = list(permuation)
        print(image_list)
        i = 0
        for item in image_list:
            with open(str(i) + '.jpg', 'wb') as handler:
                header_image_bytes = FileOperator(self.__image_header).read_byte()
                handler.write(header_image_bytes)
                for image in item:
                    image_bytes = FileOperator(image).read_byte()
                    handler.write(image_bytes)
            i += 1

if __name__ == '__main__':
    image_header = '.\material\QmXh6p3DGKfvEVwdvtbiH7SPsmLDfL7LXrowAZtQjkjw73.jpg'
    image_fragments = ['.\material\Qme7fkoP2scbqRPaVv6JEiaMjcPZ58NYMnUxKAvb2paey2',
                       '.\material\QmfUbHZQ95XKu9vd5XCerhKPsogRdYHkwx8mVFh5pwfNzE',
                       '.\material\QmU59LjvcC1ueMdLVFve8je6vBY48vkEYDQZFiAbpgX9mf',
                       '.\material\QmXFSNiJ8BdbUKPAsu3oueziyYqeYhi3iyQPXgVSvqTBtN',
                       '.\material\QmZkF524d8HWfF8k2yLrZwFz9PtaYgCwy3UqJP5Ahk5aXH']

    image_combine = ImageCombination(image_header, image_fragments)
    image_combine.combine()