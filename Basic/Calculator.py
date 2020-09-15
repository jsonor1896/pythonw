def view_start():
    """
    计算器显示界面
    """
    print('你需要使用的计算机功能')
    print('1.+')
    print('2.-')
    print('3.*')
    print('4./')

def add(v1, v2):
    """
    加法
    :param v1: 操作数1
    :param v2: 操作数2
    :return: 两个操作数之和
    """
    return v1 + v2


def sub(v1, v2):
    """
    减法
    :param v1: 操作数1
    :param v2: 操作数2
    :return: 两个操作数只差
    """
    return v1 - v2


def div(v1, v2):
    """
    除法
    :param v1: 被除数
    :param v2: 除数
    :return: 如果除数为0，返回None，否则返回计算值
    """
    if v2 == 0:
        return None
    else:
        return v1 / v2


def mul(v1, v2):
    """
    乘法
    :param v1: 操作数1
    :param v2: 操作数2
    :return: 两个操作数乘法结果
    """
    return v1 * v2


def get_calc_func_index():
    """
    获取用户选择的功能键值索引
    :return: 用户选择的功能值
    """
    while True:
        calc_func_index = input()
        if calc_func_index in ['1', '2', '3', '4']:
            return calc_func_index

        print('不支持该项功能，请重新选择')


def get_proc_number_pair():
    """
    获取用户输入的操作数信息
    :return: (操作数1，操作数2)
    """
    vals = input('请按照格式"1,2"(不包括引号)输入计算值').split(',')

    return int(vals[0]), int(vals[1])


# 计算功能函数字典
CalcFuncDictionary = {
    '1': add,
    '2': sub,
    '3': div,
    '4': mul
}


def simple_calc():
    """
    计算器
    """
    view_start()
    calc_func_index = get_calc_func_index()
    val1, val2 = get_proc_number_pair()
    result = CalcFuncDictionary[calc_func_index](val1, val2)
    print('计算结果为', result)


if __name__ == '__main__':
    simple_calc()



