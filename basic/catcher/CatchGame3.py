import os
import random


def paint_step(name, step):
    print(name, end='  ')
    print('%2d' % step, end=' ')
    i = 0
    while i < step:
        print('-', end='')
        i = i + 1
    print()


def paint(s1, s2, nexts, gos=0):
    os.system("cls")
    paint_step('player1', s1)
    paint_step('player2', s2)
    print('This is the turn of ', nexts)
    if gos > 0:
        print('The player get the count = ', gos)


def forward(step):
    gos = random.randint(1, 6)
    step += gos
    finished = False

    if step > 50:
        step = 100 - step
    elif step == 50:
        finished = True

    return step, gos, finished


if __name__ == '__main__':
    step1 = 0
    step2 = 0

    paint(step1, step2, 'player1')

    while True:
        input()
        step1, gos, finished = forward(step1)
        paint(step1, step2, 'player2', gos)
        if finished:
            print('player1 win the game')
            break

        input()
        step2, gos, finished = forward(step2)
        paint(step1, step2, 'player1', gos)
        if finished:
            print('player2 win the game')
            break

