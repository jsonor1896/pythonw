from concurrent.futures.thread import ThreadPoolExecutor
import queue
import threading
import time


def invokeFuncIntervalTime(func):
    start = time.time()
    func()
    print(time.time() - start)


def runCell(n):
    print('task begin {}'.format(n + '\n'), end='')
    time.sleep(2)
    print('task finish {}'.format(n) + '\n', end='')


def threadInvokeFunc():
    def func():
        print('-----------simple thread invoke with function-------------')
        t1 = threading.Thread(target=runCell, args=('t1',))
        t2 = threading.Thread(target=runCell, args=('t2',))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    invokeFuncIntervalTime(func)


def threadInheritClass():
    class MyThread(threading.Thread):
        def __init__(self, name, sleepTime):
            super(MyThread, self).__init__()
            self.num = name
            self.sleepTime = sleepTime

        def run(self):
            print('task {} start'.format(self.num))
            time.sleep(self.sleepTime)
            print('task {} done'.format(self.num))

    def func():
        t1 = MyThread('t1', 2)
        t2 = MyThread('t2', 4)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    print('-----------simple thread invoke with class-------------')
    invokeFuncIntervalTime(func)


def threadInvokeMore():
    def func():
        listThreads = []
        for i in range(50):
            t = threading.Thread(target=runCell, args=('t%s' % i,))
            listThreads.append(t)
            t.start()

        for th in listThreads:
            th.join()

    invokeFuncIntervalTime(func)


def threadDaemon():
    def func():
        for i in range(50):
            t = threading.Thread(target=runCell, args=('t%s' % i,))
            t.setDaemon(True)  # 将和主线程一起结束
            t.start()

        print(threading.current_thread(), threading.active_count())

    invokeFuncIntervalTime(func)


def threadWaitForKeyPress():
    stop = False

    def workingMethod():
        while not stop:
            print('i am working', time.time())
            time.sleep(2)

        print('i am working fininded')

    t = threading.Thread(target=workingMethod)
    t.start()
    input()
    stop = True
    time.sleep(5)


sharedResourceNotLocked = 0


def threadNotLock():
    def increase():
        global sharedResourceNotLocked
        for i in range(1000000):
            sharedResourceNotLocked += 1

    def decrement():
        global sharedResourceNotLocked
        for i in range(1000000):
            sharedResourceNotLocked -= 1

    t1 = threading.Thread(target=increase)
    t2 = threading.Thread(target=decrement)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    global sharedResourceNotLocked
    print(sharedResourceNotLocked)


sharedLock = threading.Lock()


def threadHasLock():
    """
    Take care of different of Lock between RLock
    http://www.zhangdongshengtech.com/article-detials/182
    """
    def increase():
        global sharedResourceNotLocked
        for i in range(1000000):
            sharedLock.acquire()
            sharedResourceNotLocked += 1
            sharedLock.release()

    def decrement():
        global sharedResourceNotLocked
        for i in range(1000000):
            sharedLock.acquire()
            sharedResourceNotLocked -= 1
            sharedLock.release()

    t1 = threading.Thread(target=increase)
    t2 = threading.Thread(target=decrement)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    global sharedResourceNotLocked
    print(sharedResourceNotLocked)


def threadQueue():
    q = queue.Queue(maxsize=10)

    def producer():
        count = 1
        while True:
            q.put('task %s' % count)
            print('generate task %s\n' % count, end='')
            count = count + 1
            time.sleep(1)

    def consumer(name):
        while True:
            print('[%s] get [%s] and do it...\n' % (name, q.get()), end='')
            time.sleep(3)

    p1 = threading.Thread(target=producer)
    c1 = threading.Thread(target=consumer, args=('dog',))
    c2 = threading.Thread(target=consumer, args=('cat',))
    p1.start()
    c1.start()
    c2.start()


def threadFuturePool():
    """
    https://docs.python.org/zh-cn/3/library/concurrent.futures.html
    """

    def func():
        print('------------thread future pool executor----------')
        with ThreadPoolExecutor(max_workers=3) as executor:
            future = executor.submit(runCell, '1')
            print(future.result())

    invokeFuncIntervalTime(func)


