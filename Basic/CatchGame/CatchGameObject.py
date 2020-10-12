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
        self.__step = 0
        self.__total_step = total_step

    @property
    def name(self):
        return self.__name

    def go_forward(self):
        """
        玩家前进
        """
        self.__step = random.randint(1, 6)
        self.__current_pos = self.__step + self.__current_pos

        if self.__current_pos > self.__total_step:
            self.__current_pos = self.__total_step - (self.__current_pos - self.__total_step)

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
        print(self.__name, '-' * self.__current_pos, self.__current_pos )


def view(players):
    os.system('cls')
    for item in players:
        item.dipslay()


def players_go(players):
    for player in players:
        input(f'请按回车键前进{player.name}')
        player.go_forward()
        view(players)

        if player.has_rearched():
            return player

    return None


if __name__ == '__main__':
    players = (Player('player1', 50), Player('player2', 50))

    while True:
        view(players)
        player = players_go(players)
        if player:
            print(f'{player.name}赢得了比赛')
            break











