from enum import Enum
from random import random


class RobotLevel(Enum):
    EASY = 1,
    NORMAL = 2,
    HARD = 3


class FingerGuessRobot(object):
    Const_Dict = {
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

    def __init__(self, level: RobotLevel):
        if level == RobotLevel.EASY:
            self.__rate = [50, 80, 100]
        elif level == RobotLevel.NORMAL:
            self.__rate = [35, 70, 100]
        else:
            self.__rate = [20, 50, 100]

    def __random_game_result(self):
        val = random.randint(1, 100)
        for i in range(0, len(self.__rate)):
            if val < self.__rate[i]:
                return str(i - 1)

    def finger(self, your_finger):
        result = self.__random_game_result()
        robot_finger = FingerGuessRobot.Const_Dict[your_finger][result]

        return result, robot_finger
