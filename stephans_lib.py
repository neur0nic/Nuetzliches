#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Bla Bla Bla

"""
import pip
required_pkgs = ['termcolor', 'bcrypt']
installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]
for package in required_pkgs:
    if package not in installed_pkgs:
        pip.main(['install', '--user', package])

from termcolor import colored
from urllib.request import urlopen
from time import time, sleep, strftime  # time, sleep for tests
import string
from random import choice
import pickle
from os import urandom, listdir, getcwd, remove
from binascii import b2a_hex
import bcrypt


def colored_bar(current, total):
    """ Colored bar: Can be used for programs, that need some time.
        :param current:     is the current point of iterations; int or float
        :param total:       is the total amount if iteration; int or float
    """
    i = round((current / total) * 100, 1)
    strdone = colored(int(round(i, 0)) * '█', 'green')
    strundone = colored((100 - int(round(i, 0))) * '█', 'red')
    totstr = "|%s%s|%s%%" % (strdone, strundone, str(i))
    print(totstr, end='\r')
    if current == total: print()


def ascii_bar(current, total):
    """ Uncolored bar: Can be used for programs, that need some time.
        :param current:     is the current point of iterations; int or float
        :param total:       is the total amount if iteration; int or float
    """
    i = round((current / total) * 100, 1)
    strdone = int(round(i, 0)) * '#'
    strundone = (100 - int(round(i, 0))) * '-'
    totstr = "|%s%s|%s%%" % (strdone, strundone, str(i))
    print(totstr, end='\r')
    if current == total: print()


def scrape(url):
    """ Downloads the HTML-Code from an specific site.
        Works just on some sites
        :param url:     compete URL; str
        :return:        the HTML-Code; str
    """
    with urlopen(url) as f:
        code = f.read()
        htmltext = code.decode("ISO-8859-1")
    return htmltext


def ddhhmmss(seconds):
    """ Converts seconds in a human readable format.
        :param seconds:     seconds; int or float
        :return :           days, hours, minutes, seconds; tuple
    """
    s_per_d = 86400
    s_per_h = 3600
    s_per_m = 60
    d = int(seconds / s_per_d)
    h = int((seconds % s_per_d) / s_per_h)
    m = int(((seconds % s_per_d) % s_per_h) / s_per_m)
    s = round((((seconds % s_per_d) % s_per_h) % s_per_m), 2)
    return d, h, m, s


def pwgenerator(length):
    """ Little password generator
        :param length:      digits of the password; int
        :return:            a password; str
    """
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    pw = (''.join(choice(chars) for i in range(length)))
    return pw


class PwStorage:
    """ Store and retrieve passwords and API-keys
        Stored passwords can be dictionaries, too, e.g {'CONSUMER_KEY': 'AKLSDJKJSDA', 'CONSUMER_SECRET': 'ASDKJAJSKDHUIWD'}
        Passwords are neither encrypted nor salted. They are binary stored in plain text.
        Never add the files user.lst and pw.list to the repository.
    """
    def __init__(self):
        self.wdir = getcwd()
        self.userfile = self.wdir + '/user.lst'
        self.pwfile = self.wdir + '/pw.lst'

    def store_passwd(self, username, password):
        """
            :param username:    unique username; str
            :param password:    password; str, list, tuple, dict
        """
        index = str(b2a_hex(urandom(5))).replace('b\'', '').replace('\'', '')
        files = listdir(self.wdir)
        user = {username: index}
        pw = {index: password}

        if self.userfile in files:
            with open(self.userfile, 'rb') as fr:
                userdir = pickle.load(fr)
        else: userdir = {}

        if self.pwfile in files:
            with open(self.pwfile, 'rb') as fr:
                pwdir = pickle.load(fr)
        else: pwdir = {}

        userdir.update(user)
        pwdir.update(pw)

        with open(self.userfile, 'wb') as fr:
            pickle.dump(userdir, fr)
        with open(self.pwfile, "wb") as fr:
            pickle.dump(pwdir, fr)

    def read_passwd(self, username):
        """
            :param username:    unique username; str
            :return:            the password; str, list, tuple, dict
        """
        try:
            with open(self.userfile, 'rb') as fr:
                userdir = pickle.load(fr)
            with open(self.pwfile, 'rb') as fr:
                pwdir = pickle.load(fr)
            index = userdir[username]
            pw = pwdir[index]
        except FileExistsError:
            pw = ''
        return pw


class LoginManager:
    """ Managing passwords for users
        Prototype for managing users
            username        a username, str
            password        a password, str
    """

    def __init__(self):
        self.wdir = getcwd()
        self.userfile = self.wdir + '/huser.lst'
        self.pwfile = self.wdir + '/hpw.lst'

    def register_user(self, username, password):
        """
            :param username:    unique username; str
            :param password:    password; str
        """
        userdir, pwdir = self.open_db()
        if username not in userdir:
            hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.store_password(username, hashed_passwd)
        else:
            print('User already exists.')

    def authenticate_user(self, username, password):
        """
            :param username:    unique username; str
            :param password:    password; str
            :return:            True or False
        """
        pw = self.read_password(username)
        if bcrypt.checkpw(password.encode('utf-8'), pw):
            return True
        else:
            return False

    def open_db(self):
        folder = listdir(self.wdir)
        if self.userfile in folder:
            with open(self.userfile, 'rb') as fr: userdir = pickle.load(fr)
        else:
            userdir = {}
        if self.pwfile in folder:
            with open(self.pwfile, 'rb') as fr: pwdir = pickle.load(fr)
        else:
            pwdir = {}
        return userdir, pwdir

    def store_password(self, username, hashed_passwd):
        index = str(b2a_hex(urandom(5))).replace('b\'', '').replace('\'', '')
        user = {username: index}
        pw = {index: hashed_passwd}
        userdir, pwdir = self.open_db()
        userdir.update(user)
        pwdir.update(pw)

        with open(self.userfile, 'wb') as fr: pickle.dump(userdir, fr)
        with open(self.pwfile, "wb") as fr: pickle.dump(pwdir, fr)

    def read_password(self, username):
        try:
            with open(self.userfile, 'rb') as fr: userdir = pickle.load(fr)
            with open(self.pwfile, 'rb') as fr: pwdir = pickle.load(fr)
            index = userdir[username]
            pw = pwdir[index]
        except FileExistsError:
            pw = ''
        return pw


def add_to_log(errormessage):
    """ For writing an Error.log file
        Creates a log-file with time and error message
        :param errormessage:    the error message; str
    """
    if isinstance(errormessage, str):
        time = strftime("%Y-%m-%d: %H:%M:%S - ")
        with open('Error.log', 'a') as fa: fa.write(time + errormessage)
    else:
        pass


def damn_artifacts(query):
    """ Clean strings from artifacts
        :param query:   text with artifacts because of encoding errors; str
        :return:        text without artifacts; str
    """
    z = query.replace('Ã¤', 'ä').replace('Ã¼', 'ü').replace('Ã¶', 'ö').replace('Ã', 'ß').replace('â', '’') \
        .replace('Ã©', 'é').replace('Ã§', 'ç').replace('Ã¸', 'ø').replace('Ã¥', 'å').replace('Ã', 'Ü') \
        .replace('Ã', 'Ä').replace('Ã', 'Ö').replace('Ã¨', 'è').replace('Â½', '½').replace('Ã´', 'ô') \
        .replace('Ã²', 'ò').replace('Ãª', 'ê').replace('Â´', '´').replace('Ã«', 'ë').replace('Ã®', 'î') \
        .replace('Ã¹', 'ù').replace('Ã', 'Ø').replace('Ã ', 'à').replace('Ã¢', 'â').replace('Ã ', 'à') \
        .replace('Ã³', 'ó').replace('Ã¯', 'ï').replace('Ãº', 'ú').replace('Ã', 'É').replace('Ã', 'Ò')
    return z


""" Test-functions
    In this section are test functions and examples
"""


def test_bars():
    for i in range(0, 251):
        colored_bar(i, 250)
        sleep(0.05)

    for i in range(0, 251):
        ascii_bar(i, 250)
        sleep(0.05)


def test_scrape():
    url = 'https://www.archlinux.org'
    text = scrape(url)
    start = text.find('<title>') + 7
    end = text.find('</title>')
    print(text[start:end])


def test_ddhhmmss():
    start_time = time()
    sleep(5)
    duration = ddhhmmss((time() - start_time))
    print("--- %sd %sh %sm %ss ---" % duration)


def test_passwd():
    x = pwgenerator(15)
    print('Generated password: %s' % x)


def test_pwstorage():
    pws = PwStorage()
    pws.store_passwd(username='testuser', password={'ACCESS_TOKEN': 'testpasswd'})
    print(pws.read_passwd(username='testuser')['ACCESS_TOKEN'])
    remove(pws.userfile)
    remove(pws.pwfile)


def test_loginmngr():
    lmngr = LoginManager()
    lmngr.register_user(username='testuser', password='testpasswd')
    print(lmngr.authenticate_user(username='testuser', password='testpasswd'))
    remove(lmngr.userfile)
    remove(lmngr.pwfile)


def test_error():
    add_to_log('Test Error')
    with open('Error.log', 'r') as f: msg = f.readlines()
    for i in msg: print(i)
    remove('Error.log')


def test_damnartifacts():
    print(damn_artifacts('LÃ¶wenbrÃ¤u'))


if __name__ == '__main__':
    # test_bars()
    # test_scrape()
    # test_ddhhmmss()
    # test_passwd()
    # test_pwstorage()
    # test_loginmngr()
    # test_error()
    # test_damnartifacts()
    pass
