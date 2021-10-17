import random

if __name__ == '__main__':

    print('欢迎来到猜拳AI游戏世界')

    gl = {
            '0': [80, 90],       # 智障
            '1': [60, 80],       # 精通
            '2': [30, 65],       # 大神
            '3': [10, 50]        # 无敌
        }

    hard = input('请选择电脑难度, 0.智障 1.精通, 2.大神, 3. 无敌')

    for i in range(0, 9):
        choose = input('请选择 1.石头 2.剪刀 3.布   ')
        num = random.randint(0, 99)
        print('概率是 ', num)
        if choose == '1':
            if num < gl[hard][0]:
                print('电脑出 剪刀')
                print('你赢了')
                break
            elif num < gl[hard][1]:
                print('电脑出 石头')
                print('平局')
            else:
                print('电脑出 布')
                print('你输了')
        elif choose == '2':
            if num < gl[hard][0]:
                print('电脑出 布')
                print('你赢了')
                break
            elif num < gl[hard][1]:
                print('电脑出 石头')
                print('你输了')
            else:
                print('电脑出 剪刀')
                print('平局')
        else:
            if num < gl[hard][0]:
                print('电脑出 石头')
                print('你赢了')
                break
            elif num < gl[hard][1]:
                print('电脑出 石头')
                print('你输了')
            else:
                print('电脑出 布')
                print('平局')
