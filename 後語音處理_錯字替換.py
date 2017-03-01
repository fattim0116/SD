# encoding=utf-8

import jieba.analyse
import re
import csv
import cgi

jieba.set_dictionary("dict.txt.big.txt")
jieba.analyse.set_stop_words("stop_words.txt")
jieba.load_userdict("user_dict.txt")

query = cgi.FieldStorage()
urlDetail = query.getvalue('sen','None')

sentence = "%s" %urlDetail
_sentence = sentence

########## Delete repeat words########################
for words in sentence:
    if (re.search('%s%s' % (words, words), sentence)):
        delword = re.compile('%s%s' % (words, words))
        sentence = delword.sub('%s' % words, sentence)


########## Def #######################################
def replace(tags, names, excNum):
    global sentence
    rechars = re.compile(tags)
    sentence = rechars.sub(names, sentence)
    if (excNum == 0):
        return True
    else:
        return "Stop"


def string_match_one_word(names, index):
    global sentence

    for nums in range(index, len(sentence) - (len(names) - 1)):
        checkMatch = 0
        words = []

        for num in range(nums, nums + len(names)):
            words += sentence[num]
        for i in range(0, len(names)):
            if (words[i] == names[i]):
                checkMatch += 1
            if (checkMatch == 1):
                sentence = list(sentence)
                for i in range(0, len(names)):
                    if (words[i] != names[i]):
                        sentence[nums + i] = names[i]
                sentence = "".join(sentence)
                return True


def string_match_two_words(names, index):
    global sentence

    for nums in range(index, len(sentence) - (len(names) - 1)):
        checkMatch = 0
        words = []

        for num in range(nums, nums + len(names)):
            words += sentence[num]
        for i in range(0, len(names)):
            if (words[i] == names[i]):
                checkMatch += 1
        if (checkMatch == len(names)):
            sentence = list(sentence)
            for i in range(0, len(names)):
                if (words[i] != names[i]):
                    sentence[nums + i] = names[i]
            sentence = "".join(sentence)
            return "Stop"
        elif (checkMatch > 1 and checkMatch != len(names)):
            sentence = list(sentence)
            for i in range(0, len(names)):
                if (words[i] != names[i]):
                    sentence[nums + i] = names[i]
            sentence = "".join(sentence)
            return True


def returnIndex(tag):
    global choise, menuElements
    for i in range(0, menuElements):
        if (tag == choise[i][0]):
            return i


def giveErrorTips(y, indexOfInsert):
    global sentence
    sentence = list(sentence)
    sentence.insert(indexOfInsert, "(或%s)" % y)
    sentence = "".join(sentence)
    return (indexOfInsert + len(y))


def storePlus(word):
    with open("dictData.csv", "r")as file:
        reader = csv.reader(file)
        for row in reader:
            for char in row:
                if (word == char):
                    return row


######################################################

tags = jieba.analyse.extract_tags(sentence, 10)

print("--------------------------\n")
print("Sentence:" + sentence)
print("--------------------------\n")
print("Tags:" + ",".join(tags))
print("--------------------------\n")

menu = {"麥香雞",
        "麥香魚",
        "雙層牛肉吉士堡",
        "可樂"}  # 建立詞庫供掃描

menuElements = len(menu)

choise = [[None] * (menuElements) for i in range(menuElements)]
for i in range(0, len(tags)):
    choise[i][0] = tags[i]
######################################################

if (sentence.count(" ") == 0):
    for chars in tags:
        arrIndex = returnIndex(chars)
        check = False
        recheck = True
        temp = None
        choiseIndexTwo = 1
        choiseIndexOne = 1
        for i in range(0, len(chars)):
            if (check == "Stop"):
                break
            for j in range(i + 1, len(chars)):
                if (check == "Stop"):
                    break
                for eles in menu:
                    if (re.search('%s.*%s' % (chars[i], chars[j]), eles)):
                        if (chars == eles):
                            check = replace(chars, eles, 1)
                            break
                        keep = True
                        for x in range(1, len(choise[arrIndex])):
                            if (eles == choise[arrIndex][x]):
                                keep = False
                                break
                        if (keep):
                            choise[arrIndex][choiseIndexTwo] = eles
                            choiseIndexTwo += 1

        for element in range(1, len(choise[arrIndex])):
            if (temp == choise[arrIndex][element]):
                choise[arrIndex][element] = None
                break
        if (choiseIndexTwo == 2):
            check = replace(chars, choise[arrIndex][choiseIndexTwo - 1], 0)
            choise[arrIndex][choiseIndexTwo - 1] = None
        elif (choiseIndexTwo > 2):
            check = True

        if (check == False):
            for i in range(0, len(chars)):
                for eles in menu:
                    if (re.search(chars[i], eles)):
                        keep = True
                        for x in range(1, menuElements):
                            if (eles == choise[arrIndex][x]):
                                keep = False
                        if (keep):
                            choise[arrIndex][choiseIndexOne] = eles
                            choiseIndexOne += 1
            if (choiseIndexOne == 2):
                check = replace(chars, choise[arrIndex][choiseIndexOne - 1], 0)
                choise[arrIndex][choiseIndexOne - 1] = None
            elif (choiseIndexOne > 2):
                check = True

        if (check == False):
            # print(chars + "can't be determined!!")
            # sentence = replace(chars,"xxx",0)

            for i in range(0, len(chars)):
                plusIndexCheck = 0
                findWord = ""
                checkArray = []
                checkArray = storePlus(chars[i])
                for eles in menu:
                    eleList = list(eles)
                    if (plusIndexCheck > 1):
                        plusIndexCheck = 0
                        break
                    for index in range(0, len(checkArray)):
                        if (eleList.count(checkArray[index]) > 0):
                            plusIndexCheck += 1
                            findWord = eles
                            break
                if (plusIndexCheck == 1):
                    check = replace(chars, findWord, 0)
                    break

else:
    for chars in tags:
        changeIndex = _sentence.index(chars)
        arrIndex = returnIndex(chars)
        check = False
        recheck = True
        temp = None
        choiseIndexTwo = 1
        choiseIndexOne = 1
        for i in range(0, len(chars)):
            if (check == "Stop"):
                break
            for j in range(i, len(chars)):
                if (check == "Stop"):
                    break
                for eles in menu:
                    if (check == "Stop"):
                        break
                    if (re.search('%s.*%s' % (chars[i], chars[j]), eles)):
                        if (recheck):
                            if ((changeIndex - len(eles)) > 1):
                                check = string_match_two_words(eles, (changeIndex - len(eles)))
                            else:
                                check = string_match_two_words(eles, changeIndex)
                            temp = eles
                            recheck = False
                        else:
                            keep = True
                            for x in range(1, menuElements):
                                if (eles == choise[arrIndex][x]):
                                    keep = False
                                    break
                            if (keep):
                                choise[arrIndex][choiseIndexTwo] = eles
                                choiseIndexTwo += 1

        for element in range(1, len(choise[arrIndex])):
            if (temp == choise[arrIndex][element]):
                choise[arrIndex][element] = None
                break
        if (check == False):
            for i in range(0, len(chars)):
                for eles in menu:
                    if (re.search(chars[i], eles)):
                        keep = True
                        for x in range(1, menuElements):
                            if (eles == choise[arrIndex][x]):
                                keep = False
                        if (keep):
                            choise[arrIndex][choiseIndexOne] = eles
                            choiseIndexOne += 1
            if (choiseIndexOne == 2):
                if ((changeIndex - len(choise[arrIndex][choiseIndexOne - 1])) > 1):
                    check = string_match_one_word(choise[arrIndex][choiseIndexOne - 1],
                                                  (changeIndex - len(choise[arrIndex][choiseIndexOne - 1])))
                else:
                    check = string_match_one_word(choise[arrIndex][choiseIndexOne - 1], changeIndex)
                choise[arrIndex][choiseIndexOne - 1] = None
            elif (choiseIndexOne > 2):
                check = True

        if (check == False):
            print(chars + "can't be determined!!")
            sentence = replace(chars, "xxx", 0)
######################################################

for row in choise:
    if (row.count(None) < (menuElements - 1)):
        for i in range(0, len(row[0])):
            plusIndexCheck = 0
            findWord = ""
            checkArray = []
            checkArray = storePlus((row[0])[i])
            for eles in menu:
                eleList = list(eles)
                if (plusIndexCheck > 1):
                    plusIndexCheck = 0
                    break
                for index in range(0, len(checkArray)):
                    if (eleList.count(checkArray[index]) > 0):
                        plusIndexCheck += 1
                        findWord = eles
                        break
            if (plusIndexCheck == 1):
                check = replace(row[0], findWord, 0)
                break


newtags = jieba.analyse.extract_tags(sentence, 10)
"""
#errorTemp = []
#for i in range(0, menuElements):
#    if (len(choise[i]) > 1):
#        for j in range(1, len(choise[i])):
#            if (choise[i][j] != None):
#                errorTemp.append(choise[i][0])
#                errorTemp.append(choise[i][j])
#
#lastInsert = []
#insertLenRecord = []
#doInsert = False
#plusIndex = 0
#
#for i in range(0, len(errorTemp), 2):
#    k = _sentence.index(errorTemp[i]) + len(errorTemp[i])
#    for j in range(0, len(lastInsert)):
#        if (k > lastInsert[j]):
#            doInsert = True
#            plusIndex += insertLenRecord[j]
#    if (doInsert):
#        lastInsert.append(giveErrorTips(errorTemp[i + 1], k + plusIndex))
#    else:
#        lastInsert.append(giveErrorTips(errorTemp[i + 1], k))
#    insertLenRecord.append(len(errorTemp[i + 1]) + 3)
#    doInsert = False
#    plusIndex = 0
"""

print("New sentence:" + sentence + "\n")

_newtags = jieba.analyse.extract_tags(sentence, 10)
######################################################

print("--------------------------\n")
print("New tags:" + ",".join(_newtags))
