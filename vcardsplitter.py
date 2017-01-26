# Aus einer mehrere VCards machen

while True:
    try:
        INPUTFILENAME = str(input('Input Filename: '))
        INPUTFILENAME = INPUTFILENAME + ".vcf"
        #print(INPUTFILENAME)
        break
    except:
        pass

#print("geschafft0")


def CutCard(Card, j):
    File = open(Card, "r")
    Text = File.readlines()
    #print("geschafft0.5")
    # Card lesen
    i = j
    #print(i)
    while True:
        if 'BEGIN:VCARD' in Text[i]:
            Beginn = i
            break
        elif i > 100000:
            break
        else:
            i += 1
    #print('Beginn = ', Beginn)
    i = j + 1
    while True:
        if 'END:VCARD' in Text[i]:
            Ende = i
            break
        elif i > 100000:
            break
        else:
            i += 1
    #print('Ende = ', Ende)
    i = j
    while True:
        if 'FN:' in Text[i]:
            Titel = i
            break
        elif i > 100000:
            break
        else:
            i += 1
    #print('Titel = ', Titel)
    File.close
    #print("geschafft1")

    # Card Schreiben
    #Name = int(len(Text[Titel]) - 3) * "X"
    Name = ""
    XTitel = Text[Titel]
    #print(XTitel)
    for i in range(3, len(XTitel)):
        if " " in XTitel[i]:
            Name += "_"
        elif i is (len(XTitel) - 1):
            Name += ".vcf"
        else:
            Name += XTitel[i]
    NEWFILENAME = str(Name)
    #print(NEWFILENAME)
    Neu = open(NEWFILENAME, "w")
    for i in range(Beginn, (Ende + 1)):
        Neu.write((Text[i]))
    Neu.close
    print(Name)
    return(i)

i = 0
zaehler = 0
while True:
    try:
        i = CutCard(INPUTFILENAME, i)
        zaehler += 1
        #print(zaehler)
        if zaehler > 1000000:
            break
        else:
            pass
    except:
        print('Fertig! ')
        break