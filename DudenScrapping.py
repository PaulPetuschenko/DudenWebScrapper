import requests
import bs4
import time
import logging, sys 
import json

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

meanings = []
frequencies = []
words = []
wordart = []
grammar = []
Duden = {}

link = ['https://www.duden.de/rechtschreibung/d_Korrekturzeichen_fuer_tilgen']

def getLinkElement(res):
    soup = bs4.BeautifulSoup(res,"lxml")
    hookup = soup.find_all("nav", class_="hookup__group")
    return bs4.BeautifulSoup(str(hookup[1]), "lxml").select(".hookup__link")[1]
 
def getLink(link):
    a =  bs4.BeautifulSoup(str(link)).find_all('a')
    return "https://www.duden.de/" + str(a[0].get('href'))    

def writeWord(res):
    try:
        soup = bs4.BeautifulSoup(res,"lxml")
        word = soup.find("span", class_="lemma__main")
        return word.contents[0]
    
    except: 
        return ""

def extractTextFromLink(a):
    try:
        return a.contents[0]
    except:
        return a

def extractMeaning(word):
    out = word.contents[2].contents[0]

    try:
        out += word.contents[2].contents[1].contents[0]
    except: 
        pass

    try:
        out += word.contents[2].contents[2]
    except:
        pass

    return out

def extractTextFromManyInputs(lis):
    out = []
    for el in range(len(lis)):
        full_str = ""
        for elm in range(len(lis[el].contents)):
            full_str += str(extractTextFromLink(lis[el].contents[elm]))
        out.append(full_str)
    return out        

def writeMeaning(res):
    soup = bs4.BeautifulSoup(res,"lxml")
    
    if soup.find("div", id="bedeutung") != None:
        word = soup.find("div", id="bedeutung")
        return extractMeaning(word)
    
    elif soup.find("div", id="bedeutungen") != None:
        word = soup.find_all("div", class_="enumeration__text")
        return extractTextFromManyInputs(word)
    
    else:
        return ""
    pass

def writeGrammar(res):
    
    pass

def writeFrequency(res):
    try:
        soup = bs4.BeautifulSoup(res,"lxml")
        word = soup.find("span", class_="shaft__full")
        return word.contents[0]
    except: 
        return ""

def writeArticle(res):
    try:
        soup = bs4.BeautifulSoup(res,"lxml")
        word = soup.find("dd", class_="tuple__val")
        return word.contents[0]
    except:
        return ""
        
def parseDuden():
    parsedHTML = requests.get(link[0]).text

    Duden.update({writeWord(parsedHTML).replace("\xad", ""):[len(writeFrequency(parsedHTML)), writeArticle(parsedHTML), writeMeaning(parsedHTML), link[0]]})
    
    link[0] = getLink(getLinkElement(parsedHTML))
    pass


for a in range(0, 1000):
    time.sleep(0)
    parseDuden()

time.sleep(0)

with open('Duden.json', 'w') as f:
    json.dump(Duden, f)
