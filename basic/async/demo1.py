"""
协程learning demo 1
"""


def loop_list():
    print('---------loop list----------')
    for x in [1, 2, 3]:
        print(x, end=' ')


def loop_dict():
    print('---------loop dict----------')
    prices = {'GOOG': 490.10,
              'AAPL': 145.23,
              'YHOO': 21.71}
    for key in prices:
        print(key, end=' ')


def loop_string():
    print('---------loop string----------')
    s = "Yow"
    for c in s:
        print(c, end=' ')


def loop_file_line():
    print('---------loop file line----------')
    with open('demo1.py') as f:
        for line in f.readlines():
            print(line, end=' ')


def loop_with_func():
    print('---------loop with func----------')
    print(sum([1, 2, 3]))
    print(min([1, 2, 3]))
    print(max([1, 2, 3]))


def generate1_simple():
    print('---------generate1----------')
    items = [4, 5, 6]
    it = iter(items)
    print(it.__next__())
    print(it.__next__())
    print(it.__next__())


def generate2_next():
    print('---------generate2----------')
    items = [4, 5, 6]

    it = iter(items)
    while True:
        try:
            val = it.__next__()
            print(val)
        except StopIteration:
            break


def generate3_countdowniter():
    class CountDown(object):

        def __init__(self, count):
            self.count = count
            self.start = self.count

        def __iter__(self):
            return self

        def __next__(self):
            if self.count <= 0:
                self.count = self.start
                raise StopIteration

            n = self.count
            self.count -= 1
            return n

    print('---------generate3 countdown iterater----------')
    c = CountDown(10)
    for i in c:
        print(i, end=' ')


def generate4_yield_countdown():
    def yield_countdown(n):
        while n > 0:
            yield n
            n -= 1

    print('\n---------generate4 yield countdown----------')
    for i in yield_countdown(10):
        print(i, end=' ')


def generate5_expression1():
    a = [1, 2, 3, 4]
    """
    for x in a:
        yield 2 * x
    """

    c = (2 * x for x in a)

    """
    (expression for i in s if condition) 
    
    for i in s:
        if condition:
            yield expression
    """
    print('\n---------generate expression----------')
    for x in c:
        print(x, end=' ')


def generate6_yieldfrom():
    def countdown(start):
        while start > 0:
            yield start
            start = start - 1

    def countdown_yieldfrom():
        for i in range(1, 10):
            yield from countdown(i)
            print()

    print('\n---------generate6 yield from----------')
    for n in countdown_yieldfrom():
        print(n, end=' ')


def generate7_yieldfrom_send():
    def average_gen():
        total = 0.0
        count = 0
        average = 0.0

        while True:
            new_num = yield average
            if new_num is None:
                break
            count += 1
            total += new_num
            average = total / count

    def proxy_gen():
        while True:
            yield from average_gen()

    print('\n---------generate7 yield from----------')
    calc_average = proxy_gen()
    next(calc_average)
    print(calc_average.send(10))
    print(calc_average.send(20))
    print(calc_average.send(30))


if __name__ == '__main__':
    loop_list()
    loop_dict()
    loop_string()
    loop_file_line()
    loop_with_func()
    generate1_simple()
    generate2_next()
    generate3_countdowniter()
    generate4_yield_countdown()
    generate5_expression1()
    generate6_yieldfrom()
    generate7_yieldfrom_send()
