import sys
import os
import requests
from bs4 import BeautifulSoup

import time
import csv


def return_diki_word(word):
    diki_word = {
        "word" : word,
        "mowa" : "",
        "tlumaczenia" : [
            {
                "znaczenie" : [""],
                "zdania" : [
                    {
                        "orginal" : "",
                        "tlumaczenie" : "",
                    }
                ]
            }
        ]
    }

    try:
        os.mkdir("audio")
    except OSError:
        pass
    
    if word == '': return diki_word

    ans = requests.get('https://www.diki.pl/slownik-angielskiego?q=' + word)
    soup = BeautifulSoup(ans.content, 'html.parser')
    if not soup:
        return "err"
    znaczeniaSoup = []
    if souptwo:=soup.findAll("div", {"class": "diki-results-left-column"}):
        souptwo = souptwo[0]
        znaczeniaSoup = souptwo.findAll("li")
    elif souptwo:=soup.findAll("div", {"class": "dikiBackgroundBannerPlaceholder"}):
        souptwo = souptwo[0]
        znaczeniaSoup = souptwo.findAll("div", {"class": "dictionaryEntity"})
    else:
        print("ERROR")

    znaczenia = []
    for nr_znaczenia in range(len(znaczeniaSoup)):
        znaczenie = {}
        znaczenie["znaczenie"] = [item.text for item in znaczeniaSoup[nr_znaczenia].findAll("span", {"class": "hw"})]
        zdania = znaczeniaSoup[nr_znaczenia].find_all("div", {"class": "exampleSentence"}) #.contents[0].strip().replace("\r\n","")
        tlumaczeniezdania = znaczeniaSoup[nr_znaczenia].find_all("span", {"class": "exampleSentenceTranslation"}) #.text.strip().replace("\r\n","")
        merged_zdania = [{"orginal" : zdania[i].contents[0].strip().replace("\r\n",""),"tlumaczenie" : tlumaczeniezdania[i].text.strip().replace("\r\n","")} for i in range(0, len(zdania))] 
        znaczenie["zdania"] = merged_zdania
        znaczenia.append(znaczenie)
    if znaczeniaSoup:
        diki_word["tlumaczenia"] = znaczenia
        #mowa:
        # if (r:=requests.get("https://www.diki.pl/images-common/en/mp3/" + word.strip().replace(" ", "_").lower() + ".mp3")).status_code != 404:
        #     open(os.path.join("audio", word.strip().replace(" ", "_").lower() + ".mp3"), 'wb').write(r.content)
        #     diki_word["mowa"] = "[sound:" + word.strip().replace(" ", "_").lower() + ".mp3]"
        # elif (r:=requests.get("https://www.diki.pl/images-common/en-ame/mp3/" + word.strip().replace(" ", "_").lower() + ".mp3")).status_code != 404:
        #     open(os.path.join("audio", word.strip().replace(" ", "_").lower() + ".mp3"), 'wb').write(r.content)
        #     diki_word["mowa"] = "[sound:" + word.strip().replace(" ", "_").lower() + ".mp3]"

    return diki_word

def toExcel():
    #to excel
    iterator = 0
    with open('INput.csv', encoding='utf-8-sig') as csvfile:
        with open('output.csv',mode="w", encoding='utf-8-sig',newline='') as csvoutput:
            googleinput = csv.reader(csvfile, delimiter=';', dialect='excel')
            outputWrite = csv.writer(csvoutput, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in googleinput:
                anki_slowo = return_diki_word(row[0])
                time.sleep(0.1)
                tlumaczenia = ""
                for i in range(len(anki_slowo["tlumaczenia"])):               
                    tlumaczenia += ", ".join(anki_slowo["tlumaczenia"][i]["znaczenie"]).strip().replace("\n","") + "<br>"
                outputWrite.writerow(row + [tlumaczenia] + [anki_slowo["mowa"]])
                print(str(iterator) + ". " + str(row + [tlumaczenia]))
                iterator+=1

def toAnki():
    pass
    #jebac

