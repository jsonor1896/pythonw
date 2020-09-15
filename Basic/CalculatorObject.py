class CalculatorObject(object):
    """
    计算器类，实现两个操作数的加减乘除
    """

    def __init__(self, val1, val2):
        """
        构造函数，设置两个操作数的值
        :param val1: 操作数1
        :param val2: 操作数2
        """
        self.__val1 = val1
        self.__val2 = val2


    def add(self):
        """
        加法
        :return:两个操作数之和
        """
        return self.__val1 + self.__val2


    def sub(self):
        """
        减法，操作数1-操作数2
        :return: 两个操作数只差
        """
        return self.__val1 - self.__val2


    def div(self):
        """
        除法，操作数1 / 操作数2
        :return: 两个操作数除法，如果操作数为0，返回除法结果
        """
        if self.__val2 == 0:
            return None
        else:
            return self.__val1 / self.__val2


    def mul(self):
        """
        乘法
        :return:两个操作数的乘法
        """
        return self.__val1 * self.__val2


