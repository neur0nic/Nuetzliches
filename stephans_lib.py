''' Progressbar for the Terminal.
    Can be used for programs, that need some time.
        current     is the current point of iterations. int or float
        total       is the total amount if iteration. int or float
'''
from time import sleep
from termcolor import colored


def progressbar(current, total):
    i = round((current / total) * 100, 1)
    strdone = int(round(i, 0)) * '█'
    strundone = (100 - int(round(i, 0))) * '█'
    totstr = "|" + colored(strdone, 'green') + colored(strundone, 'red') + "| " + str(i) + "%"
    print(totstr, end='\r')
    if current == total: print()

''' Thread to abort program.
    Can be used to stop progams with the 'enter'-key.
'''
from threading import Thread


def waittoabort():
    list = []
    abort = Thread(target=stopp, args=(list,))
    abort.start()
