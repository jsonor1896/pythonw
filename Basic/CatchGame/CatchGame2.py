import os
import random


def display_player(players):
    os.system('cls')
    for key, player in players.items():
        print('player name', player['name'], ':', '-' * player['current_step'], player['current_step'])


def go_forward(player, total_step):
    step = random.randint(1, 6)
    dest_step = player['current_step'] + step

    if dest_step < total_step:
        player['current_step'] = dest_step
    else:
        player['current_step'] = total_step - (dest_step - total_step)

    return step


if __name__ == '__main__':
    playerDict = {
        'player1': {
            'name': 'player1',
            'current_step': 0
        },
        'player2': {
            'name': 'player2',
            'current_step': 0
        }
    }

    display_player(playerDict)

    while True:
        for key, player in playerDict.items():
            input('this is the turn of player: ' + player['name'])
            step = go_forward(player, 50)
            display_player(playerDict)
            print('roll the number is ', step)

            if player['current_step'] == 50:
                print('you win the game', player['name'])
                exit(1)



