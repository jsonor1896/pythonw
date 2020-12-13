import platform

import psutil

def get_info_by_platform():
    # 系统架构，系统32/64bit
    print(platform.architecture())
    # 机器的详细信息：(system, node, release, version, machine, processor)
    print(platform.uname())

    # 当前的python版本号
    print(platform.python_version())


def get_info_by_psutil():
    # 逻辑核心
    print(psutil.cpu_count())
    # 物理核心
    print(psutil.cpu_count(False))

    # 内存
    print(psutil.virtual_memory())
    # 交换内存
    print(psutil.swap_memory())

    print(psutil.disk_partitions(all=True))

    print(psutil.users())

    for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time']):
        print(proc.info)

if __name__ == '__main__':

    get_info_by_psutil()


