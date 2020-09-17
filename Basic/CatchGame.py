import os
import random

Player1 = 0
Player2 = 0
TotalStep = 50

def go_forward(player_step):
    step = random.randint(1, 6)
    current_step = player_step + step

    if current_step > TotalStep:
        current_step = TotalStep - (current_step - TotalStep)

    return step, current_step


def view(step):
    os.system('cls')
    print('player1 ', Player1, ':', '-' * Player1)
    print('player2 ', Player2, ':', '-' * Player2)
    if step > 0:
        print('The step is ', step)


if __name__ == '__main__':
    step1 = step2 = 0
    while True:
        view(step2)
        if Player2 == TotalStep:
            print('player 2 win the game')
            break
        input('this is the turn of player1')
        step1, Player1 = go_forward(Player1)
        view(step1)
        if Player1 == TotalStep:
            print('player 1 win the game')
            break
        input('this is the turn of player2')
        step2, Player2 = go_forward(Player2)
