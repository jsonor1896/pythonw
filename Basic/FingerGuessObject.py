from enum import Enum
from random import random


class RobotLevel(Enum):
    EASY = 1,
    NORMAL = 2,
    HARD = 3


class FingerGuessRobot(object):

    Const_Dict = {
        '剪刀': {
            '1': '布',
            '-1': '石头',
            '0': '剪刀'
        },
        '石头': {
            '1': '剪刀',
            '-1': '布',
            '0': '石头'
        },
        '布': {
            '1': '石头',
            '-1': '剪刀',
            '0': '布'
        }
    }

    def __init__(self, level:RobotLevel):
        if level == RobotLevel.EASY:
            self.__result_rate = [50, 80, 100]
        elif level == RobotLevel.NORMAL:
            self.__result_rate = [35, 70, 100]
        else:
            self.__result_rate = [20, 50, 100]


    def __random_game_result(self):
        random_val = random.randint(1, 100)
        if random_val < self.__result_rate[0]:
            return 1
        elif random_val < self.__result_rate[1]:
            return 0
        else:
            return -1


    def finger(self, your_finger):
        result = self.__random_game_result()
        robot_finger = FingerGuessRobot.Const_Dict[your_finger][str(result)]

        return result, robot_finger

