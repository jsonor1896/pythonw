import os
import random

players = []
current_player = 0


def go():
    player = players[current_player]
    gos = random.randint(1, 6)
    player['step'] = player['step'] + gos
    if player['step'] > 50:
        player['step'] = 100 - player['step']
    elif player['step'] == 50:
        player['finished'] = True

    return gos


def paint(gos=0):
    global current_player
    os.system('cls')
    for player in players:
        print(player['name'], end='  ')
        print(player['step'], end='  ')
        print(player['step'] * '-')

    if gos != 0:
        print(players[current_player]['name'], 'go ', gos)
        if not players[current_player]['finshed']:
            current_player = current_player + 1 if current_player + 1 < count else 0
        else:
            return

    print('it is the turn of ', players[current_player]['name'])


if __name__ == '__main__':
    count = int(input('please choose the number of the player, do not greate then 9\r\n'))
    for i in range(0, count):
        players.append(
            {
                'name': "player%d" % i,
                'step': 0,
                'finished': False
            }
        )

    paint()

    while True:
        input()
        gos = go()
        paint(gos)
        if players[current_player]['finished']:
            print(players[current_player]['name'], 'win the game')
            break
