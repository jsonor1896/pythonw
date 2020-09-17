import os
import random


class Player:

    def __init__(self, name, total_step):
        self.__name = name
        self.__current_pos = 0
        self.__prev_pos = 0
        self.__prev_step = 0
        self.__total_step = total_step


    @property
    def name(self):
        return self.__name


    @property
    def total_step(self):
        return self.__total_step


    @property
    def current_pos(self):
        return self.__current_pos


    @property
    def prev_step(self):
        return self.__prev_step


    @property
    def prev_pos(self):
        return self.__prev_pos


    def go_forward(self):
        self.__prev_step = random.randint(1, 6)
        self.__prev_pos = self.__current_pos
        self.__current_pos = self.__prev_step + self.__current_pos

        if self.__current_pos > self.__total_step:
            self.__current_pos = self.__total_step - (self.__current_pos - self.__total_step)

        return True if self.__current_pos == self.__total_step else False


def view(players):
    os.system('cls')
    for item in players:
        print(item.name, item.prev_pos, '+', item.prev_step, '=', item.current_pos, '-' * item.current_pos)



if __name__ == '__main__':
    players = (Player('player1', 50), Player('player2', 50))

    while True:
        view(players)
        for player in players:
            input('按回车前进 {name}'.format(name=player.name))
            result = player.go_forward()
            view(players)
            if result:
                exit('胜利 {name}'.format(name=player.name))











