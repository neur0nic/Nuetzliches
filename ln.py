# -*- coding: utf-8 -*-
import os

os.system("fdupes -r ./ >> ./doppel.log")

fr = open("doppel.log", "r")
text = fr.readlines()
#print(type(text))
fr.close

ln = "ln -fsr "
code = []
count = 0

try:
    for i in range(0, len(text)):
        #print(i)
        #print(text[i] + "\n" + "---")
        if "\n" is text[i] and "\n" is text[i + 3]:
            if "\n" in text[i + 1]:
                text[i + 1] = text[i + 1].replace("\n", "")
            if " " in text[i + 1]:
                text[i + 1] = text[i + 1].replace(" ", "\ ")
            if "(" in text[i + 1]:
                text[i + 1] = text[i + 1].replace("(", "\(")
            if ")" in text[i + 1]:
                text[i + 1] = text[i + 1].replace(")", "\)")
            if "\n" in text[i + 2]:
                text[i + 2] = text[i + 2].replace("\n", "")
            if " " in text[i + 2]:
                text[i + 2] = text[i + 2].replace(" ", "\ ")
            if "(" in text[i + 2]:
                text[i + 2] = text[i + 2].replace("(", "\(")
            if ")" in text[i + 2]:
                text[i + 2] = text[i + 2].replace(")", "\)")
            code.append(ln + text[i + 1] + " " + text[i + 2])
except:
    pass

#print(code)

fw = open("symlinker.sh", "w")
fw.write("#!/bin/bash\n")
for i in code:
    fw.write(i + "\n" + "\n")
fw.close

#x = "Nein"
#while x != "ja":
    #x = input("Code OK? ")

os.system("chmod +x ./symlinker.sh")
#os.system("./symlinker.sh")

exit()
