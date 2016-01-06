# -*- coding: utf-8 -*-
import re


#############################
#Dieses Programm war nur für den Abgleich zwischen Lexikon und Medulla gedacht
#############################

def readLexicon(file):
    varianten = {}
    try:
        lexiconfile = open(file, 'r', encoding="utf-8")
        lexicon = lexiconfile.read()
        for line in lexicon.split('\n'):
            liste = line.split('\t')
            lemma = re.sub(r' ','',liste[-2])
            wortart = liste[-1]
            for lexem in liste:
                varianten[re.sub(r' ','',lexem)] = (lemma,wortart)
        return varianten
    except:
        print("Error while reading Lexicon")

def cleaning(word):
    cleaned_word = "".join(c for c in word if c not in ('!',')','(','.',':',' ', '?','/',' '))
    return cleaned_word

lexiconfile = "lexikon_tagged.tsv"
nhdlex = readLexicon(lexiconfile)

#file = "medulla_zsm.xml"
#xmlfile = open(file, 'r', encoding="utf-8")
#xml = xmlfile.read()

#uncomment = re.compile(r'<.*?>',re.DOTALL)
#rein = re.sub(uncomment,'', xml)
#rein = re.sub(r'\#\.tz','ꜩ',rein)
#rein = re.sub(r'\#\.tz','tz',rein)
#rein = re.sub(r'\#\.s','ſ',rein)
#rein = re.sub(r'\#\.s','s',rein)
#rein = re.sub(r'\[.\]','',rein)
#rein = re.sub(r'\#\'','', rein)
#rein = re.sub(r'%\-(.)',r'\1̅', rein)
xmlfile = open('medulla_konv_ohne.xml','r', encoding="utf-8")
rein = xmlfile.read()

TokenInMedulla = 0
TokenAbgedeckt = 0
ctext = []
frequenzliste = {}
for word in rein.split():
    cword = cleaning(word)

    ctext.append(cword)
    if cword in nhdlex.keys():
        TokenAbgedeckt +=1
    else:
        if cword in frequenzliste.keys():
            frequenzliste[cword] = frequenzliste[cword]+1
        else:
            frequenzliste[cword] = 1
    TokenInMedulla += 1

s1 = set(nhdlex.keys())
s2 = set(ctext)
TypesInMedulla = len(s2)
TypesAbgedeckt = len(s2.intersection(s1))

print(TokenInMedulla)
print(TokenAbgedeckt)
print(TypesInMedulla)
print(TypesAbgedeckt)
print(frequenzliste)
tliste = []
for x in frequenzliste.keys():
    tliste.append((frequenzliste[x], x))
tliste.sort(key=lambda x: x[0],reverse=True)
print(tliste)