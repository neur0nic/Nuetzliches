# -*- coding: utf-8 -*-
import os


def bashing(x):
    if " " in x:
        x = x.replace(" ", "\ ")
    if "(" in x:
        x = x.replace("(", "\(")
    if ")" in x:
        x = x.replace(")", "\)")
    if "\n" in x:
        x = x.replace("\n", "")
    if "%" in x:
        x = x.replace("%", "\%")
    return x

os.system('echo "\n" > ./doppel.log')
os.system("fdupes -r ./ >> ./doppel.log")

fr = open("doppel.log", "r")
text = fr.readlines()
# print(type(text))
# print(text)
fr.close()

code = []
try:
    for i in range(0, len(text)):
        if "\n" is text[i]:
            start = i + 2
            for z in range(1, 11):
                if "\n" is text[i + z]:
                    stop = i + z
                    break
                else:
                    continue
            for j in range(start, stop):
                text[j] = bashing(text[j])
                code.append("rm -rdv " + text[j])
        else:
            continue
except:
    pass

fw = open("remover.sh", "w")
fw.write("#!/bin/bash\n")
for i in code:
    fw.write(i + "\n")
fw.close()

os.system("chmod +x ./remover.sh")
os.system("./remover.sh")

exit()