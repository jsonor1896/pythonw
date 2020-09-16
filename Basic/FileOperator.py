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


    def read_byte(self, length):
        with open(self.__file_path, 'rb') as handler:
            array_bytes = handler.read(length)
            return array_bytes


    def write_new(self, content):
        with open(self.__file_path, 'w') as handler:
            handler.write(content)


    def write_arrays(self, array):
        with open(self.__file_path, 'w') as handler:
            for item in array:
                handler.write(item)

