# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import re


#Funktion: liest lexikon-file
#parameter: dateiname
#rückgabe: lexikon; Lexikonterm -> (lemma,wortart)
#lexikon: variante1 ... varianteN Lemma Wortart
def readLexicon(file):
    varianten = {}
    try:
        lexiconfile = open(file, 'r', encoding="utf-8")
        lexicon = lexiconfile.read()      
        for line in lexicon.split('\n'):
            liste = line.split('\t')
            lemma = re.sub(r' ','',liste[-2])
            wortart = liste[-1]
            for lexem in liste[:-1]:
                varianten[re.sub(r' ','',lexem)] = (lemma,wortart)
        return varianten
    except:
        print("Error while reading Lexicon")

#Funktion: bereinigt ein Wort von Sonderzeichen und führt lemmatisierung mit Lexikon durch
#parameter: das zu bereinigende Wort, Lexikon (optional)
#Rückgabe: das bereinigte (evt. lemmatisierte) Wort
def cleaning(word,lexicon=0):
    cleaned_word = "".join(c for c in word if c not in ('!',')','(','.',':',' ', '?','/',' '))

    #wenn lexikon vorhanden:
    if lexicon != 0:
        # wenn das wort im lexikon ist
        if cleaned_word in lexicon:
            #wird das wort durch das im lexikon gespeicherte lemma ersetzt
            cleaned_word = lexicon[cleaned_word][0]
    return cleaned_word

#Funktion: Berechnet den Mittelwert einer Liste
#Parameter: Liste mit Datenpunkten
#Rückgabe: gemittelter Wert
#!!Vermutlich ist die Funktion unnötig, es gibt sicher eine vorgefertigte Python-Methode
#!!Namensgebung ireführend
def simpleMovingAverage(data):
    n = len(data)
    summe = 0
    for i in data:
        summe += i
    return summe/n

#Funktion: berechnet den TTR-Verlauf
#Parameter: Textstring, Anzahl an Datenpunkte über die gemittelt werden soll(zum glätten)
#Rückgabe: Liste mit TTR-Werten, "geglätteten" TTR-Werten, sowie dem Text als Liste
#!!sinnvoller: Trennung von TTR,average und Textliste
#!!lexikon müsste als Parameter übergeben werden !
#!!textliste enthält noch nicht die "bereinigten" Wörter
def computeTTR(text,average):
    #lexikongenerierung
    nhd_lexicon = readLexicon('lexikon_tagged.tsv')
    #Dictionary für Types, TTR-Array sowie zwei Zähler (types udn tokens)
    #werden initialisiert und auf null/leer gesetzt
    types = {} 
    typecount = 0
    tokencount = 0
    simple_ttr = []
    averagedsimple_TTR = []
    
    #Beginne Schleife
    #text.split(' ') zerteilt das Dokument in "Wörter"
    #bzw. "splittet" nach jedem Leerzeichen
    textlist=text.split(' ')
    for token in textlist:
        #fügt gerade betrachtetes Wort/Token in die Typeliste ein
        # ODER erhöht die Vorkommen des Types im Dictionary
        word = cleaning(token,nhd_lexicon)
        if word in types:
            types[word] = types[word]+1
        else:
            types[word] = 1
            #für jeden neuen Type wird die Typeanzahl erhöht
            typecount = typecount+1
        
        #Am Ende jedes Schleifendurchgangs wird der Tokenzähler erhöht
        tokencount = tokencount+ 1
        #Und der derzeitige TTR-Wert an das Array angehängt
        simple_ttr.append(typecount/tokencount)
        if len(simple_ttr) > average-1:
            averagedsimple_TTR.append(simpleMovingAverage(simple_ttr[-average:]))
    return simple_ttr, averagedsimple_TTR, textlist

#Funktion: Berechnet die lokalen Maxima im TTR-Graph
#Parameter: Liste mit (TTR-)Werten
#Rückgabe: Liste mit Maxima
#!!Funktion ist mittlerweile unnötig, wird nicht mehr verwendet
def getPeaks(data):
    points = []
    x = 1
    while x < len(data)-1:
        if (data[x]>data[x-1]) & (data[x]>data[x+1]):
            difference = data[x]-data[x-1]
            peak = [x,difference]            
            points.append(peak)
        x += 1
    return points

#Funktion: Berechnet den Steigungsverlauf
#Parameter: Liste mit (TTR-)Werten
#Rückgabe: Steigungsverlauf
def slope(data):
    points = []
    x = 1
    while x < len(data)-1:
        points.append(data[x+1]-data[x-1])
        x += 1
    
    return points

#Funktion: findet die Bereiche, in möglicherweise ein Topic eingeführt wird
#Parameter: Steigungsverlauf(liste), minimale Dauer der positiven Steigung (int), Anzahl erlaubter "dips" ins negative (int)
#Rückgabe: TopicIntroducingAreas (liste: (start, ende))
#!!Parameter allowedDips ist eventuell unnötig
def typeIntroducingAreas(slope,minLengthOfAscent, allowedDips):
    i = 0
    areas = []
    while i < len(slope):
        if slope[i] >= 0:
            dips = 0
            y = 1
            while dips < allowedDips:
                if slope[i+y] < 0:
                    dips += 1
                y += 1
            if y >= minLengthOfAscent:
                areas.append([i, i+y])
        i += y
    return areas

#Funktion: plottet die 3 Graphen
#Parameter: TTR-Verlauf (liste), TopicAreas [Liste: (start,ende)], Steigungsverlauf (liste), Text (liste)
#!!onclickevent generiert Fehlermeldung, wenn man außerhalb des plots klickt
def plot(ttr,topic,slope,text):
#    plt.ylabel('TTR')
#    plt.xlabel('Tokens')
    #plt.plot(ttr)
#    for peak in peaks:
#        plt.axvspan(peak[0], peak[0]+5, facecolor='g', alpha=0.5)
    fig = plt.figure()
    ax_ttr = fig.add_subplot(311, xlim=(1, len(ttr)), ylim=(0.0, 1.0))
    ax_ttr.plot(ttr)
    ax_slope = fig.add_subplot(312, xlim=(1, len(ttr)))
    ax_slope.plot(slope)
    ax_topic = fig.add_subplot(313, xlim=(1, len(ttr)))
    for area in topic:
        ax_topic.axvspan(area[0], area[1], facecolor='g', alpha=0.5)

    # Function to be called when mouse is clicked
    def on_click(event):
        if (event.xdata>0) & (event.xdata<len(ttr)):
            print(event.xdata)
            print(text[int(event.xdata)])
            #fig.canvas.draw()
    
    # Connect the click function to the button press event
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()


#########################################################Beginn des Anweisungsteil#####################################

#verwendet noch alte datei mit xml-tags
#daher, zu allererst bereinigung
file = "medulla_zsm.xml"
xmlfile = open(file, 'r', encoding="utf-8")
xml = xmlfile.read()
uncomment = re.compile(r'<.*?>',re.DOTALL)
rein = re.sub(uncomment,'', xml)
#rein = re.sub(r'\#\.tz','ꜩ',rein)
rein = re.sub(r'\#\.tz','tz',rein)
#rein = re.sub(r'\#\.s','ſ',rein)
rein = re.sub(r'\#\.s','s',rein)
rein = re.sub(r'\[.\]','',rein)
rein = re.sub(r'\#\'','', rein)
rein = re.sub(r'%\-(.)',r'\1̅', rein)

#Aufruf der Analysefunktionen
analysis = computeTTR(rein,1)
averagedTTR = analysis[1]
textlist = analysis[2]
peaks = getPeaks(averagedTTR)
slope = slope(averagedTTR)
topic = typeIntroducingAreas(slope,10,1)
#Plotting
plot(averagedTTR,topic, slope,textlist)




