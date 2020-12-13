import random

FingerNames = ['剪刀', '石头', '布']

FingerGameDict = {
    '剪刀': {
        '1' : '布',
        '-1': '石头',
        '0' : '剪刀'
    },
    '石头': {
        '1' : '剪刀',
        '-1': '布',
        '0' : '石头'
    },
    '布' : {
        '1' : '石头',
        '-1': '剪刀',
        '0' : '布'
    }
}

FingerGameLevel = {
    'win': 30,
    'equ': 70
}


def show_game_start_view():
    print('*' * 30)
    print(' 猜拳游戏现在开始 ')
    print(' 你将拥有10次机会和AI进行竞赛')
    print('*' * 30)


def choose_game_level():
    level = 0
    while True:
        level = input('请选择游戏难度, 1. 简单， 2. 中等， 3. 地狱\n')
        if level in ['1', '2', '3']: break
        print('请重新选择')

    FingerGameLevel['win'] = (4 - int(level)) * 15
    FingerGameLevel['eql'] = (3 - int(level)) * 15


def user_input_finger():
    while True:
        finger_index = input('请选择你的出拳 0. 剪刀， 1. 石头， 2. 布\n')
        if finger_index in ['0', '1', '2']:
            finger_name = FingerNames[int(finger_index)]
            print('你的选择是', finger_name)
            return finger_index, finger_name

        print("你的选项错误，请重新选择")


def random_game_result():
    rate = random.randint(0, 99)
    if rate <= FingerGameLevel['win']:
        return 1
    elif rate <= FingerGameLevel['equ']:
        return 0
    else:
        return -1


ResultCHName = ['失败', '平局', '胜利']


def finger_game():
    show_game_start_view()
    choose_game_level()

    play_count = 10
    while play_count >= 0:
        play_count -= 1
        finger_index, finger_name = user_input_finger()
        game_result = random_game_result()
        robot_finger = FingerGameDict[finger_name][str(game_result)]

        print('机器人出：', robot_finger)
        print('结果是：', ResultCHName[game_result + 1])
        if game_result == 1: break

        print('剩余次数', play_count)
        print()

    print('游戏结束')


if __name__ == '__main__':
    finger_game()
