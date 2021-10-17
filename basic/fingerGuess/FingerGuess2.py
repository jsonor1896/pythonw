import random

Probabilities = {
    '0': [80, 90],  # 智障
    '1': [60, 80],  # 精通
    '2': [30, 65],  # 大神
    '3': [10, 50]  # 无敌
}

Probability = []

DictOfName = {
    '1': '石头',
    '2': '剪刀',
    '3': '布'
}

DictOfResult = {
    '石头': {
        '1': '剪刀',
        '0': '石头',
        '2': '布',
    },
    '剪刀': {
        '1': '布',
        '0': '剪刀',
        '2': '石头'
    },
    '布': {
        '1': '石头',
        '0': '剪刀',
        '2': '布'
    }
}


def randomResult():
    num = random.randint(0, 99)
    if num < Probability[0]:
        return '1'
    elif num < Probability[1]:
        return '0'
    else:
        return '2'


if __name__ == '__main__':
    print('欢迎来到猜拳AI游戏世界')
    hard = input('请选择电脑难度, 0.智障 1.精通, 2.大神, 3. 无敌')
    Probability = Probabilities[hard]

    print(Probability)
    for i in range(0, 9):
        choose = DictOfName[input('请选择 1.石头 2.剪刀 3.布   ')]
        result = randomResult()
        robots = DictOfResult[choose][result]
        print('电脑出', robots)
        if result == '1':
            break
