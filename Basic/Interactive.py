"""
ArgumentParser的用法
"""
from argparse import ArgumentParser


def demo1():
    """
    参数：description 在调用-h的时候对脚本的描述
    """
    parser = ArgumentParser(description='demo1')
    parser.add_argument('integers', type=str, help='传入的数字')
    args = parser.parse_args()

    print(args)
    print(args.integers)        # 通过类属性的方式调用传入的参数
    # print(args.integers + 1)  # 该函代码会报错，因为已经确定该参数的类型是str类型


def demo2():
    """
    传入多个参数的调用
    """
    parser = ArgumentParser(description='demo2')
    parser.add_argument('integers', type=int, nargs='+', help='传入的是数组')     # nargs='+' 表示传入的至少一个参数
    args = parser.parse_args()

    print(args)
    print(args.integers)        # 此时获取的integers参数是一个数组


def demo3():
    """
    参数位置测试
    根据参数的数量进行分配，要求每个参数必须都有值的情况下去配置每个参数应该获得多少个值
    """
    parser = ArgumentParser(description='demo3')
    parser.add_argument('p1', type=str, nargs='+', help='姓')
    parser.add_argument('p2', type=str, help='名')
    parser.add_argument('p3', type=str, nargs='+', help='号')
    args = parser.parse_args()

    print(args)
    print(args.p1, args.p2, args.p3)


def demo4():
    """
    可选参数以及默认值，以及缩写方式
    """
    parser = ArgumentParser(description='demo4')
    parser.add_argument('-f', '--family', type=str, default='张', help='姓')
    # 如果设置了require=True，那么默认值是无用的
    parser.add_argument('-n', '--name',   type=str, default='三', help='名', required=True)
    args = parser.parse_args()

    print(args)
    print(args.family, args.name)



if __name__ == '__main__':
    demo4()