import csv

import utility
import dictionaries

def calculatePatientAcctNumConfidence(patientAcctNum1, patientAcctNum2):
    if patientAcctNum1 == "" or patientAcctNum2 == "":
        return None
    distance = utility.levenshtein(patientAcctNum1, patientAcctNum2)
    confidence = 1/pow(distance+1,0.15*distance)
    return confidence

def calculateFullNameConfidence(first1, last1, first2, last2):
    if (first1 == '' or first2 == '') and (last1 != '' and last2 != ''):
        return calculateNameConfidence(last1, last2)
    elif (first1 != '' and first2 != '') and (last1 == '' or last2 == ''):
        return calculateNameConfidence(first1, first2)
    elif ((first1 == '' or first2 == '') and (last1 == '' or last2 == '')):
        return None
    else:
        total = 0
        if utility.compareFirstLastSwap(first1, last1, first2, last2):
            total += 0.2
        total += calculateNameConfidence(first1, first2) * 0.2
        total += calculateNameConfidence(last1, last2) * 0.6
        return total

def calculateNameConfidence(name1, name2):
    total = 0

    if utility.compareByAbbrevWord(name1, name2):
        total += 0.1
    
    if utility.compareWordsWithoutSpecialChars(name1, name2):
        return 1
    if utility.compareByContains(name1, name2):
        total += 0.1
    if utility.compareByDoubleMetaphone(name1, name2):
        total += 0.4
    levDistance = utility.levenshtein(name1, name2)
    levConfidence = 1/(pow(levDistance+1,0.9*levDistance)) * 0.4
    total += levConfidence
    return total

def calculateMiddleIConfidence(middle1, middle2):
    if middle1 == "" or middle2 == "":
        return None
    total = 0

    if utility.compareByAbbrevWord(middle1, middle2):
        total += 0.1
    
    if utility.compareWordsWithoutSpecialChars(middle1, middle2):
        return 1
    if utility.compareByContains(middle1, middle2):
        total += 0.1
    
    if utility.compareByDoubleMetaphone(middle1, middle2):
        total += 0.4
    levDistance = utility.levenshtein(middle1, middle2)
    levConfidence = 1/(pow(levDistance+1,0.2*levDistance)) * .4
    total += levConfidence
    return total

def calculateDOBConfidence(dob1, dob2):
    if dob1 == "" or dob2 == "":
        return None
    distance = utility.levenshtein(dob1, dob2)
    confidence = 1/pow(distance+1,0.5*distance)
    return confidence

def calculateSexConfidence(sex1, sex2):
    if sex1 == "" or sex2 == "":
        return None
    try:
        sex1 = dictionaries.sex[sex1]
    except KeyError:
        pass
    try:
        sex2 = dictionaries.sex[sex2]
    except KeyError:
        pass
    distance = utility.levenshtein(sex1, sex2)
    confidence = 1/(pow(distance+1, distance))
    return confidence

def calculateStreetConfidence(street1, street2):
    if street1 == "" or street2 == "":
        return None
    street1 = street1.split(' ')
    street2 = street2.split(' ')

    #convert street abbreviations to fully spelled out
    try:
        street1[-1] = dictionaries.streets[street1[-1]]
    except KeyError:
        pass
    try: 
         street2[-1] = dictionaries.streets[street2[-1]]
    except KeyError:
        pass
    
    if street1 == street2:
        return 1
    
    #double metaphone for each word
    for elem1, elem2 in zip(street1, street2):
        metaphoneConfidence = 0
        if elem1 == None or elem2 == None:
            break
        if utility.compareByDoubleMetaphone(elem1,elem2):
            metaphoneConfidence = 1/(max(len(street1),len(street2)))
    
    street1 = ' '.join(str(elem) for elem in street1)
    street2 = ' '.join(str(elem) for elem in street2)

    #levenshtein
    distance = utility.levenshtein(street1, street2)
    levenshteinConfidence = 1/(pow(distance+1,0.2*distance))

    return metaphoneConfidence * 0.5 + levenshteinConfidence * 0.5

def calculateCityConfidence(city1, city2):
    if city1 == "" or city2 == "":
        return None
    #calculate two fully spelled out cities
    #levenshtein
    else:
        distance = utility.levenshtein(city1, city2)

        dmetaScore = 0
    #double metaphone
        if utility.compareByDoubleMetaphone(city1, city2):
            dmetaScore = 0.5

    #calculate abbreviations
        abbreviationScore = 0
        shortenedScore = 0
        if utility.compareByAbbrevSentence(city1, city2):
            abbreviationScore = (min(len(city1),len(city2)))/5
    #calculate shortened versions (if abbreviated skip)
        elif utility.compareByContains(city1,city2):
            shortenedScore = (min(len(city1),len(city2)))/max(len(city1),len(city2))

        confidence = min(1/(pow(distance+1, distance+1)) + dmetaScore + abbreviationScore + shortenedScore, 1)
        return confidence

def calculateStateConfidence(state1, state2):
    #convert abbreviations to full states
    if state1 == "" or state2 == "":
        return None
    else:
        try: 
            state1 = dictionaries.states[state1]
        except KeyError:
            pass
        try:
            state2 = dictionaries.states[state2]
        except KeyError:
            pass
        distance = utility.levenshtein(state1, state2)
        confidence = 1/(distance+1)
        return confidence

def calculateZipConfidence(zip1, zip2):
    if zip1 == "" or zip2 == "":
        return None
    else:
        distance = utility.levenshtein(zip1, zip2) 
        confidence = 1/(pow(distance+1, distance))
        return confidence


def getConfidenceScore(row1, row2):
    row1 = [x.lower() for x in row1]
    row2 = [x.lower() for x in row2]
    row1 = [x.strip() for x in row1]
    row2 = [x.strip() for x in row2]

    PAN_WEIGHT = 0.01
    CN_WEIGHT = 0.1
    CMI_WEIGHT = 0.01
    DOB_WEIGHT = 0.06
    S_WEIGHT = 0.04
    CS1_WEIGHT = 0.2
    CS2_WEIGHT = 0.01
    CC_WEIGHT = 0.07
    CS_WEIGHT = 0.07
    CZ_WEIGHT = 0.03
    PN_WEIGHT = 0.05
    PMI_WEIGHT = 0.01
    PS1_WEIGHT = 0.16
    PS2_WEIGHT = 0.01
    PC_WEIGHT = 0.07
    PS_WEIGHT = 0.07
    PZ_WEIGHT = 0.03


    #use dictionary in case their columns are messed up
    PAN = calculatePatientAcctNumConfidence(row1[2], row2[2])
    CN = calculateFullNameConfidence(row1[3], row1[5], row2[3], row2[5])
    CMI = calculateMiddleIConfidence(row1[4], row2[4])
    DOB = calculateDOBConfidence(row1[6], row2[6])
    S = calculateSexConfidence(row1[7], row2[7]) 
    CS1 = calculateStreetConfidence(row1[8], row2[8]) 
    CS2 = calculateStreetConfidence(row1[9], row2[9])
    CC = calculateCityConfidence(row1[10], row2[10])
    CS = calculateStateConfidence(row1[11], row2[11])
    CZ = calculateZipConfidence(row1[12], row2[12])

    PN = calculateFullNameConfidence(row1[13], row1[15], row2[13], row2[15])
    PMI = calculateMiddleIConfidence(row1[14], row2[14])
    PS1 = calculateStreetConfidence(row1[16], row2[16])
    PS2 = calculateStreetConfidence(row1[17], row2[17])
    PC = calculateCityConfidence(row1[18], row2[18])
    PS = calculateStateConfidence(row1[19], row2[19])
    PZ = calculateZipConfidence(row1[20], row2[20])

    confidenceScores = [PAN,CN,CMI,DOB,S,CS1,CS2,CC,CS,CZ,PN,PMI,PS1,PS2,PC,PS,PZ]
    weights = [PAN_WEIGHT,CN_WEIGHT,CMI_WEIGHT,DOB_WEIGHT,S_WEIGHT,CS1_WEIGHT,CS2_WEIGHT,CC_WEIGHT,CS_WEIGHT,CZ_WEIGHT,
                PN_WEIGHT,PMI_WEIGHT,PS1_WEIGHT,PS2_WEIGHT,PC_WEIGHT,PS_WEIGHT,PZ_WEIGHT]

    newFactor = 0
    for score,weight in zip(confidenceScores, weights):
        if score is not None:
            newFactor += weight

    if newFactor == 0:
        newFactor = 1

    newConfidenceScores = []
    for score,weight in zip(confidenceScores, weights):
        if score is None:
            newConfidenceScores.append(0)
        else:
            newConfidenceScores.append(score * weight/newFactor)
    
    score = 0
    for s in newConfidenceScores:
        score += s
    return score

def groupByConfidenceScore(data, confidenceThreshold):
    alreadyAddedList = []
    result = []
    for row1 in data:
        if row1 in alreadyAddedList:
            continue
        group = [row1]
        alreadyAddedList.append(row1)
        for row2 in data:
            if row2 not in alreadyAddedList:
                if getConfidenceScore(row1, row2) >= confidenceThreshold:
                    group.append(row2)
                    alreadyAddedList.append(row2)
        result.append(group)
    return result
