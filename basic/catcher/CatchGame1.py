import os
import random


def go_forward(player_step, total_step):
    step = random.randint(1, 6)
    player_step = player_step + step

    if player_step > total_step:
        player_step = total_step - (player_step - total_step)

    return player_step, step


def display_input(player1, player2, input_string, step_string=None):
    os.system('cls')
    print('player1:', '-' * player1, player1)
    print('player2:', '-' * player2, player2)
    if step_string is None:
        print(step_string)
    input(input_string)


if __name__ == '__main__':
    player1_step = 0
    player2_step = 0
    total_step = 50

    display_input(player1_step, player2_step, 'the turn of player1')

    while True:
        player1_step, step = go_forward(player1_step, total_step)
        display_input(player1_step, player2_step, 'the turn of player2', f'player1 step {step}')
        if player1_step == total_step:
            print('player1 win the game')
            break

        player2_step, step = go_forward(player2_step, total_step)
        if player2_step == total_step:
            print('player2 win the game')
            break
        display_input(player2_step, player2_step, 'the turn of player1', f'player2 step {step}')
