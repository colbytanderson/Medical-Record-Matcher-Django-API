import fuzzy
import Levenshtein
import collections
import csv
import re
def removeNumbersFromWord(word):
    return ''.join([i for i in word if not i.isdigit()])

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
    return re.sub(r'\W+', '', word)

def compareByAbbrevWord(word1, word2):
	return abbrevWord(word1) == word2 or word1 == abbrevWord(word2)

def compareByAbbrevSentence(sentence1, sentence2):
	return abbrevSentence(sentence1) == sentence2 or sentence1 == abbrevSentence(sentence2)

def abbrevSentence(sentence):
	sentence = sentence.split(' ')
	result = ''
	for word in sentence:
		result += abbrevWord(word)
	return result

def abbrevWord(word):
	return word[0]

def compareByDoubleMetaphone(word1, word2):
        dmeta = fuzzy.DMetaphone(4)
        return dmeta(word1)[0] == dmeta(word2)[0] or (dmeta(word1)[1] == dmeta(word2)[1] != None and
        dmeta(word1)[1] == dmeta(word2)[1])

def levenshtein(string1, string2):
    return Levenshtein.distance(string1,string2)
