import jieba.analyse
import csv
import re
import random

jieba.set_dictionary("dict.txt.big.txt")
jieba.load_userdict("user_dict.txt")

sentence = "可樂三杯 麥香雞三份"
answerSentence = []
_answerSentence = ""
print('Content-Type: text/plain')
print("Sentence: " + sentence)
customTags = jieba.analyse.extract_tags(sentence)

menu = {"麥香雞",
        "麥香魚",
        "雙層牛肉吉士堡",
        "可樂",
        "大麥克"}

customDict = {}
numOfFood = []

#########Def####################################
def findAllNumIndex(tag):
    global sentence
    numIndexArr = [0]
    checkValid = True
    checkValidIndex = 1
    while(checkValid):
        if(checkValidIndex == 1):
            numIndexArr.append(sentence[numIndexArr[checkValidIndex-1]:].index(tag))
        else:
            numIndexArr.append(sentence[numIndexArr[checkValidIndex - 1] + len(tag):].index(tag))

        checkValidIndex += 1
        if(sentence[numIndexArr[checkValidIndex - 1] + len(tag):].index(tag) == False):
            checkValid = False
    return numIndexArr

def findFoodName(substring):
    cnt = 0
    tempFood = []
    for ele in menu:
        if(re.search(ele,substring)):
            cnt += 1
            tempFood.append(ele)
    if(cnt == 1):
        return tempFood[0]
    else:
        return tempFood

################################################
for tag in customTags:
    if(tag in menu):
        customDict[tag] = None
    else:
        numOfFood.append(tag)

for ele in numOfFood:
    reNum = re.compile(ele)
    sentence = reNum.sub(',%s,'%ele,sentence)

_sentence = sentence.split(',')
_sentence.remove('')
for index in range(0,len(_sentence)):
    chosenFood = None
    if(_sentence[index] in [None,'']):
        continue
    if(_sentence[index] in numOfFood):
        chosenFood = findFoodName(_sentence[index + 1])
        if(isinstance(chosenFood,str)):
            customDict[chosenFood] = _sentence[index]
        else:
            customDict[chosenFood[0]] = _sentence[index]
            customDict[chosenFood[1]] = _sentence[index + 2]
            _sentence[index + 2] = None
    else:
        chosenFood = findFoodName(_sentence[index])
        customDict[chosenFood] = _sentence[index+1]

    _sentence[index + 1] = None

customDictClass = customDict
probalyWord = {}
with open('probalyWord.csv','r')as wordFile:
    wordReader = csv.reader(wordFile)
    for row in wordReader:
        while(row.count('') > 0):
            row.remove('')
        probalyWord['%s'%row[0].replace('\t','')] = row[1:]

try:
    answerSentence.append(probalyWord['getTheQuestion'][random.randint(0,len(probalyWord['getTheQuestion']))])
    answerSentence.append(',')
except:
    answerSentence.append(probalyWord['getTheQuestion'][random.randint(0, len(probalyWord['getTheQuestion']) - 1)])
    answerSentence.append(',')
try:
    answerSentence.append(probalyWord['checkQuestion'][random.randint(0, len(probalyWord['checkQuestion']))])
except:
    answerSentence.append(probalyWord['checkQuestion'][random.randint(0, len(probalyWord['checkQuestion']) - 1)])
try:
    answerSentence.append(probalyWord['checkQuestion2'][random.randint(0, len(probalyWord['checkQuestion2']))])
except:
    answerSentence.append(probalyWord['checkQuestion2'][random.randint(0, len(probalyWord['checkQuestion2']) - 1)])

for key in customDict.keys():
    answerSentence.append(key)
    answerSentence.append(customDict[key])
    answerSentence.append(',')

with open('menuFactor.csv', 'r')as factorFile:
    menuReader = csv.reader(factorFile)
    for row in menuReader:
        for eles in customDict.keys():
            if (row.count(eles) > 0):
                customDictClass[eles] = row[0]

_customDictClass = []
for value in customDictClass.values():
    _customDictClass.append(value)
if(_customDictClass.count('food') > 0 and _customDictClass.count('drink') > 0):
    try:
        answerSentence.append(probalyWord['want'][random.randint(0,len(probalyWord['want']))])
    except:
        answerSentence.append(probalyWord['want'][random.randint(0, len(probalyWord['want']) - 1)])
    answerSentence.append('其他餐點嗎?')
elif(_customDictClass.count('food') == 0 and _customDictClass.count('drink') > 0):
    try:
        answerSentence.append(probalyWord['want'][random.randint(0,len(probalyWord['want']))])
    except:
        answerSentence.append(probalyWord['want'][random.randint(0, len(probalyWord['want']) - 1)])
    try:
        answerSentence.append(probalyWord['numQuestion'][random.randint(0, len(probalyWord['numQuestion']))])
    except:
        answerSentence.append(probalyWord['numQuestion'][random.randint(0, len(probalyWord['numQuestion'])) - 1])
    answerSentence.append('食物嗎?')
else:
    try:
        answerSentence.append(probalyWord['want'][random.randint(0,len(probalyWord['want']))])
    except:
        answerSentence.append(probalyWord['want'][random.randint(0, len(probalyWord['want']) - 1)])
    try:
        answerSentence.append(probalyWord['numQuestion'][random.randint(0, len(probalyWord['numQuestion']))])
    except:
        answerSentence.append(probalyWord['numQuestion'][random.randint(0, len(probalyWord['numQuestion'])) - 1])
    answerSentence.append('飲料嗎?')

for word in answerSentence:
    _answerSentence += word
#if (re.search(',$', _answerSentence)):
#    _answerSentence = re.sub(',$', '', _answerSentence)
print(_answerSentence)
