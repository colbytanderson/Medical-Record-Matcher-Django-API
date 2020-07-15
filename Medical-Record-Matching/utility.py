#code our own algorithm or use libraries?
import fuzzy #pip install fuzzy
import Levenshtein #pip install python-levenshtein
import collections
import string
import csv
import homoglyphs
import dictionaries
import re

# csv repo 1 = https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup
# csv repo 2 = https://github.com/MrCsabaToth/SOEMPI/tree/master/openempi

def streetToDoubleMetaphone(street):
    l = street.split(' ')
    try:
        l[-1] = dictionaries.streets[l[-1]]
    except KeyError:
        pass
    k = []
    for i in l:
        r = doubleMetaphone(i)
        if type(r[0]) is bytes:
            r[0] = r[0].decode('utf-8')
        if type(r[1]) is bytes:
            r[1] = r[1].decode('utf-8')
        k.append(str(r[0]) + ' ' + str(r[1]))
    
    res = ','.join(k)
    return res

def compareDoubleMetaphones(name1DM, name2DM):
    name1DM = name1DM.split(' ')
    name2DM = name2DM.split(' ')
    one = name1DM[0] == 'None' or name2DM[0] == 'None'
    two = name1DM[0] == name2DM[0] and one
    three = name2DM[1] != 'None' and name1DM[0] != 'None' and name1DM[0] == name2DM[1]
    four = one and name2DM[1] != 'None' and name1DM[1] != 'None' and name1DM[1] == name2DM[1]
    if one:
        return False
    if two:
        return True
    if three:
        return True
    if four:
        return True
    return False

def compareSentDoubleMetaphones(sent1DM, sent2DM):
	sent1DM = sent1DM.split(',')
	sent2DM = sent2DM.split(',')
	for i,j in zip(sent1DM, sent2DM):
		if not compareDoubleMetaphones(i, j):
			return False
	return True

def getCSVContents(csvFilePath):
	data = []
	with open(csvFilePath) as f:
		reader = csv.reader(f)
		for row in reader:
			data.append(row)
	return data

def compareWordsByKeyboardDistance(word1, word2):
    word1 = removeSpecialCharsFromWord(word1)
    word2 = removeSpecialCharsFromWord(word2)
    total = 0
    for i,j in zip(word1,word2):
        x1 = dictionaries.keyboard_cartesian[i]['x']
        y1 = dictionaries.keyboard_cartesian[i]['y']
        x2 = dictionaries.keyboard_cartesian[j]['x']
        y2 = dictionaries.keyboard_cartesian[j]['y']
        total += manhattanDistance(x1, y1, x2, y2)
    return total
	
def manhattanDistance(x1, y1, x2, y2):
	return abs(x2 - x1) + abs(y2 - y1)

def removeNumbersFromWord(word):
    return ''.join([i for i in word if not i.isdigit()])

def compareNameByNickname(name1, name2):
	csvFilePaths = ['nicknames1.csv','nicknames2.csv']
	allCSVData = getCSVContents(csvFilePaths[0]) + getCSVContents(csvFilePaths[1])
	for nicknameList in allCSVData:
		if name1 in nicknameList and name2 in nicknameList:
			# returns true if name 1 is a nickname for name 2 or vice versa
			return True
	return False

def compareByContains(word1, word2):
	return word1 in word2 or word2 in word1

def compareSentenceBySwap(sentence1, sentence2, separationValue):
	tokens1 = sentence1.split(separationValue)
	tokens2 = sentence2.split(separationValue)
	# returns true if the sentences have the same values in swapped order
	return collections.Counter(tokens1) == collections.Counter(tokens2)

def compareFirstLastSwap(first1, last1, first2, last2):
	# returns true if the first and last names are swapped
	return (first1 == last2) and (last1 == first2)

def compareWordsWithoutSpecialChars(word1, word2):
	# returns true if the words are the same without punctuation and whitespace
    return removeSpecialCharsFromWord(word1) == removeSpecialCharsFromWord(word2)

def removeSpecialCharsFromWord(word):
    return re.sub(r'[^a-zA-Z0-9\s]+', '', word) 

def compareByAbbrevWord(word1, word2):
	return abbrevWord(word1) == word2 or word1 == abbrevWord(word2)

def compareByVisuallySimilarChars(word1, word2):
	# rn and m. deal with it. cant go char by char
    for i,j in zip(word1,word2):
        try:
            if (not homoglyphs.Homoglyphs().get_combinations(i) == homoglyphs.Homoglyphs().get_combinations(j) or 
            dictionaries.similarChars[i] in dictionaries.similarChars[j] or i==j):
                return False
        except KeyError:
            pass
    return True

def compareByAbbrevSentence(sentence1, sentence2):
	return abbrevSentence(sentence1) == sentence2 or sentence1 == abbrevSentence(sentence2)

def abbrevSentence(sentence):
    result = ''
    temp = sentence.split(' ')
    for word in temp:
        result += abbrevWord(word)
    return result

def abbrevWord(word):
    if word == "":
        return ""
    return word[0]

def doubleMetaphone(word):
    dmeta = fuzzy.DMetaphone(4)
    res = dmeta(word)
    return res

def compareByDoubleMetaphone(word1, word2):
        dmeta = fuzzy.DMetaphone(4)
        #print(dmeta(word1)) 
        #print(dmeta(word2))
        return dmeta(word1)[0] == dmeta(word2)[0] or (dmeta(word1)[1] == dmeta(word2)[1] != None and
        dmeta(word1)[1] == dmeta(word2)[1])

def levenshtein(string1, string2):
    return Levenshtein.distance(string1,string2)

'''
SLOW: 
compareByDoubleMetaPhone
removeSpecialChars
compareWordsByKeyboardDistance
compareWordsWithoutSpecialChars
getConfidenceScore
groupByConfidenceScore
calculateFullName
calculateCityConfidence

if name and street is exactly the same, skip other confidence calls
convert everything to double metaphone array one time
if it is garbage comparison, abort
'''