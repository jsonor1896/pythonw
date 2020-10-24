class Student:
    """
    学生对象类
    """

    def __init__(self, id_num, name, age, country):
        self.__id_num = id_num
        self.__name = name
        self.__age = age
        self.__country = country

    @property
    def id_num(self):
        return self.__id_num

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def country(self):
        return self.__country

    def __str__(self):
        return f"{self.__id_num:<10} {self.__age:<4} {self.__country:<4} {self.__name:5} "


class StudentCollection:
    """
    学生属性集合类
    """

    def __init__(self, path):
        """
        初始化 stduent集合类数据，从本地文件path中读取存储的值
        :param path: 文件路径
        """
        self.__student = []
        with open(path, 'rb') as handler:
            while True:
                line = handler.readline()
                if not line: break
                items = line.decode(encoding='utf-8').strip().split(',')
                id_num, name, age, country = items[0], items[1], items[2], items[3]
                self.__student.append(Student(id_num, name, age, country))

    def __str__(self):
        txt = ''
        for std in self.__student:
            txt = txt + str(std) + '\r\n'

        return txt

    def get_by_name(self, name):
        std_list = []
        for std in self.__student:
            if std.name == name:
                std_list.append(std)

        return std_list

    def get_by_age(self, age):
        std_list = []
        for std in self.__student:
            if std.age == age:
                std_list.append(std)

        return std_list


if __name__ == '__main__':
    stds = StudentCollection('../material/student_db.txt')
    print(stds)





























