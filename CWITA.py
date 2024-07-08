import requests
from collections import defaultdict
from bs4 import BeautifulSoup
import random
# URL of the website to scrape

sentenceLength = 50
trainingSet = input("Voer URLs in. 0 - 9 voor preset: ")

if trainingSet == "0":
    urlI = "http://example.com/ http://httpbin.org/"
elif trainingSet == "1":
     urlI = "https://nl.wikipedia.org/wiki/Planten https://nl.wikipedia.org/wiki/Fotosynthese https://nl.wikipedia.org/wiki/Zaadplanten https://nl.wikipedia.org/wiki/Boom_(plant) https://nl.wikipedia.org/wiki/Struik https://nl.wikipedia.org/wiki/Bloem https://nl.wikipedia.org/wiki/Blad_(plant) https://nl.wikipedia.org/wiki/Wortel_(plant) https://nl.wikipedia.org/wiki/Stengel https://nl.wikipedia.org/wiki/Schors https://nl.wikipedia.org/wiki/Chlorofyl https://nl.wikipedia.org/wiki/Plantencel https://nl.wikipedia.org/wiki/Thylakoïde https://nl.wikipedia.org/wiki/Vaatplant https://nl.wikipedia.org/wiki/Mos https://nl.wikipedia.org/wiki/Varens https://nl.wikipedia.org/wiki/Zaden https://nl.wikipedia.org/wiki/Bol_(plant) https://nl.wikipedia.org/wiki/Knol_(plant) https://nl.wikipedia.org/wiki/Peulvrucht https://nl.wikipedia.org/wiki/Vrucht_(plant) https://nl.wikipedia.org/wiki/Bloemenkelk https://nl.wikipedia.org/wiki/Bladgroen https://nl.wikipedia.org/wiki/Cambium https://nl.wikipedia.org/wiki/Plantenhormoon https://nl.wikipedia.org/wiki/Kiem_(plant) https://nl.wikipedia.org/wiki/Zaailing https://nl.wikipedia.org/wiki/Stek_(plant) https://nl.wikipedia.org/wiki/Scheut_(plant) https://nl.wikipedia.org/wiki/Algen https://nl.wikipedia.org/wiki/Plantenziekte https://nl.wikipedia.org/wiki/Plantengemeenschap https://nl.wikipedia.org/wiki/Biodiversiteit https://nl.wikipedia.org/wiki/Plantentuin https://nl.wikipedia.org/wiki/Botanische_nomenclatuur https://nl.wikipedia.org/wiki/Fytoalexinen https://nl.wikipedia.org/wiki/Gras https://nl.wikipedia.org/wiki/Plantkunde https://nl.wikipedia.org/wiki/Plantenevolutie https://nl.wikipedia.org/wiki/Plantenveredeling https://nl.wikipedia.org/wiki/Wilde_plant https://nl.wikipedia.org/wiki/Gecultiveerde_plant https://nl.wikipedia.org/wiki/Bos https://nl.wikipedia.org/wiki/Savanne https://nl.wikipedia.org/wiki/Tropisch_regenwoud https://nl.wikipedia.org/wiki/Plantenfamilie https://nl.wikipedia.org/wiki/Succulent" 
elif trainingSet == "2":
    urlI = "https://nl.wikipedia.org/wiki/Hoofdpagina"
elif trainingSet == "3":
    urlI = "https://www.reddit.com/r/rant/comments/3uuhmo/a_long_rant_about_stuff/w"
elif len(trainingSet) < 1:
     urlI = "https://nl.wikipedia.org/wiki/Oorlog https://nl.wikipedia.org/wiki/Wereldoorlog https://nl.wikipedia.org/wiki/Russische_invasie_van_Oekra%C3%AFne_sinds_2022 https://nl.wikipedia.org/wiki/Oorlog_in_Oost-Oekra%C3%AFne"


chance = input("kansberekening. 1: dynamic. 2: vast. 3: random. ")

if not chance:
    chance = "1"
 
urlList = urlI.split(" ")
fullTrainingData = ""

for url in urlList:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the relevant information from the HTML code
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        text = paragraph.get_text()
        txt = text.strip().replace("\n", "")
        if len(txt) < 1:
            continue
        fullTrainingData += txt
    dataArraySmall = []
    prevWord = ""
    for word in fullTrainingData.split(" "):
        dataArraySmall.append({"input": prevWord, "output": word})
        prevWord = word
    dataArraySmall.sort(key=lambda x: x['input'])

    prevEntry = ""
    dataArray = []
    inpList = []
    countDict = defaultdict(int)
    # array with (input; wordname, list[{"word": word, "chance", 40}, etc etc]])
    for entry in dataArraySmall:
        if entry["input"] != prevEntry:
            for outputEntry, count in countDict.items():
                dataArray.append({"input": prevEntry, "output": outputEntry, "chance": count / len(inpList)})
            inpList.clear()
            countDict.clear()

        inpList.append(entry["output"])
        countDict[entry["output"]] += 1
        prevEntry = entry["input"]

    for outputEntry, count in countDict.items():
        dataArray.append({"input": prevEntry, "output": outputEntry, "chance": count / len(inpList)})

    prevEntry = ""
    fullDataArray = []
    for entry in dataArray:
        if entry != prevEntry:
            fullDataArray.append(entry)
        prevEntry = entry

print(str(round(len(fullTrainingData) / 1024, 2)) + " kb data")    

def getOutputFromTrainingset(query):
    expectedOutput = []
    for output in fullDataArray:
        if(output["input"] == query):
            expectedOutput.append(output)
    return expectedOutput

def returnOutputStatic(focusDataset):
    highestChance = 0
    output = ""
    for set in focusDataset:
        if(set['chance'] > highestChance):
            highestChance = set['chance']
            output = set['output']
    return output

def returnOutputRandom(focusDataset):
    random.shuffle(focusDataset)
    output = focusDataset[0]['output']
    return output

def returnOutputWeighted(focusDataset):
    highestOutput = ""
    highestChance = 0
    for set in focusDataset:
        chance = set['chance']
        if(chance > highestChance):
            highestOutput = set['output']
        if chance > random.uniform(0,1):
            return set['output']
    return highestOutput
def getOutput(focusDataset):
    if chance == "1":
        return returnOutputWeighted(focusDataset)
    elif chance == "2":
        return returnOutputStatic(focusDataset)
    elif chance == "3":
        return returnOutputRandom(focusDataset)
    else:
        print("No chance given")
        return

while True:
    index = 0
    query = input("")
    sentence = query
    while index < sentenceLength :
        focusDataset = getOutputFromTrainingset(query)
        output = getOutput(focusDataset)
        sentence += " " + output
        query = output
        index = index + 1
    print(sentence)
