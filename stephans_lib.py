''' Progressbar for the Terminal.
    Can be used for programs, that need some time.
        current     is the current point of iterations. int or float
        total       is the total amount if iteration. int or float
'''
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

    def stopp(list):
        input()
        list.append(None)

    list = []
    abort = Thread(target=stopp, args=(list,))
    abort.start()

''' Quick scrape a website
    Can be used to download a HTML website
        url     is the URL of the website.
'''
from urllib.request import urlopen


def scrape(url):
    with urlopen(url) as f:
        code = f.read()
        htmltext = code.decode("ISO-8859-1")
    return htmltext

''' Time (parts of) the program
    Needs to be integrated into the code.
    ddhhmmss transforms seconds in dd:hh:mm:ss format
'''
from time import time


def ddhhmmss(seconds):
    s_per_d = 86400
    s_per_h = 3600
    s_per_m = 60
    d = int(seconds / s_per_d)
    h = int((seconds % s_per_d) / s_per_h)
    m = int(((seconds % s_per_d) % s_per_h) / s_per_m)
    s = round((((seconds % s_per_d) % s_per_h) % s_per_m), 2)
    return d, h, m, s

start_time = time()

# Put code to measure here

duration = ddhhmmss((time()-start_time))
print("--- %s d %s h %s m %s s ---" % duration)

''' Little password generator
        length      the length of the password. int
'''
import string
from random import choice


def pwgenerator(length):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    pw = (''.join(choice(chars) for i in range(length)))
    return pw