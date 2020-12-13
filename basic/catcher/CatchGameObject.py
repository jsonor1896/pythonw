import os
import random


class Player:

    def __init__(self, name, total_step):
        """
        构造函数
        :param name: 玩家的姓名
        :param total_step: 玩家需要走的总步数
        """
        self.__name = name
        self.__current_pos = 0
        self.__total_step = total_step

    @property
    def name(self):
        """
        获取用户名
        """
        return self.__name

    def go_forward(self):
        """
        玩家前进
        """
        step = random.randint(1, 6)
        self.__current_pos = step + self.__current_pos

        if self.__current_pos > self.__total_step:
            self.__current_pos = self.__total_step - (self.__current_pos - self.__total_step)

        return step

    def has_rearched(self):
        """
        是否达到终点
        :return: 到达返回True，否则返回false
        """
        return self.__current_pos == self.__total_step

    def dipslay(self):
        """
        显示信息
        """
        print(self.__name, '-' * self.__current_pos, self.__current_pos)


class CatchGame:
    """
    你追我赶游戏
    """

    def __init__(self, *players):
        """
        构造函数
        :param players: 游戏者列表
        """
        self.__players = players

    def __show(self):
        """
        清屏显示数据
        """
        os.system('cls')
        for item in self.__players:
            item.display()

    def start(self):
        self.__show()
        while True:
            for player in players:
                input(f'{player.name}请按回车键前进')
                player.go_forward()
                self.__show()


if __name__ == '__main__':
    players = (Player('player1', 50), Player('player2', 50))
    catch_game = CatchGame(players)
    catch_game.start()
