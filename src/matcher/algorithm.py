import utility
import dictionaries
import mysql.connector
from mysql.connector import errorcode

#import database
#assume all strings all lower

#elongate all abbreviaions (rd to road, CA to california, M to male)
#remove all special chars
#lowercase all
#remove trailing and leading whitespace
def start():
    try:
        cnx = mysql.connector.connect(user='sql3329916', password='APzc3QtGkq',
                                host='sql3.freemysqlhosting.net',
                                database='sql3329916')
        cursor = cnx.cursor()
    except:
        print("Error")
        exit()
    #Creates AdaptedTable
    TABLE = {}
    TABLE['createAdaptedTable'] = (
        "CREATE TABLE IF NOT EXISTS `AdaptedData` ("
        "  `Patient Acct #` varchar(30) NOT NULL,"
        "  `First Name` varchar(30) NOT NULL,"
        "  `Full MI` varchar(15) NOT NULL,"
        "  `Last Name` varchar(30) NOT NULL,"
        "  `Date of Birth` varchar(15) NOT NULL,"
        "  `Sex` varchar(10) NOT NULL, "
        "  `Current Street 1` varchar(50) NOT NULL,"
        "  `Current Street 2` varchar(50) NOT NULL,"
        "  `Current City` varchar(30) NOT NULL,"
        "  `Current State` varchar(30) NOT NULL,"
        "  `Current Zipcode` varchar(10) NOT NULL,"
        "  `Previous First Name` varchar(30) NOT NULL,"
        "  `Previous Full MI` varchar(10) NOT NULL,"
        "  `Previous Last Name` varchar(30) NOT NULL,"
        "  `Previous Street 1` varchar(50) NOT NULL,"
        "  `Previous Street 2` varchar(50) NOT NULL,"
        "  `Previous City` varchar(30) NOT NULL,"
        "  `Previous State` varchar(30) NOT NULL,"
        "  `Previous Zipcode` varchar(10) NOT NULL,"

        "  `First Name DMeta` varchar(15) NOT NULL,"
        "  `True MI` varchar(10) NOT NULL,"
        "  `MI DMeta` varchar(15) NOT NULL,"
        "  `Last Name DMeta` varchar(15) NOT NULL,"
        "  `Current Street 1 DMeta` varchar(50) NOT NULL,"
        "  `Current Street 2 DMeta` varchar(50) NOT NULL,"
        "  `Current City Abbrev` varchar(15) NOT NULL,"
        "  `Current City DMeta` varchar(30) NOT NULL,"
        "  `Previous First Name DMeta` varchar(30) NOT NULL,"
        "  `Previous True MI` varchar(10) NOT NULL,"
        "  `Previous MI DMeta` varchar(10) NOT NULL,"
        "  `Previous Last Name DMeta` varchar(30) NOT NULL,"
        "  `Previous Street 1 DMeta` varchar(50) NOT NULL,"
        "  `Previous Street 2 DMeta` varchar(50) NOT NULL,"
        "  `Previous City Abbrev` varchar(15) NOT NULL,"
        "  `Previous City DMeta` varchar(30) NOT NULL,"
        "  `PatientID` varchar(30) NOT NULL)"
    )

    try:
        cursor.execute(TABLE['createAdaptedTable'])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
        else: 
            print(err.msg)
    else:
        print("OK")
    
    #Find number of rows
    cursor.execute('SELECT PatientID FROM `Data` ORDER BY PatientID DESC LIMIT 1')
    count = cursor.fetchone()[0]

    #insert into rows
    INSERT = {}
    RETRIEVE = {}
    patientID = ""
    for i in range(1,count+1):
        RETRIEVE['retrieve'] = (
            "SELECT * from `Data` WHERE PatientID=" + str(i)
        )
        patientID = str(i)
        cursor.execute(RETRIEVE['retrieve'])
        row = cursor.fetchone()[2:]
        insertValues = []
        #add columns into new table 
        for i in range(len(row)):
            newData = row[i].strip()
            newData = newData.lower()
            #is on sex
            if i == 5:
                try: 
                    newData = dictionaries.sex[newData]
                except KeyError:
                    pass
            #is on streets
            elif i == 6 or i == 7 or i == 14 or i == 15:
                temp = newData.split(' ')
                try:
                    temp[-1] = dictionaries.streets[temp[-1]]
                except KeyError:
                    pass
                newData = ' '.join([str(elem) for elem in temp])
            #is on state
            elif i == 9:
                try:
                    newData = dictionaries.states[newData]
                except KeyError:
                    pass
            newData = utility.removeSpecialCharsFromWord(newData)
            insertValues.append(newData)
        
        #add special columns
        row = row[1:]
        #firstNameDMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[0]))
        #True MI
        insertValues.append(utility.abbrevWord(row[1]))
        #MI DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[1]))
        #Last Name DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[2]))
        #Current Street1 DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[5]))
        #Current Street2 Dmeta
        insertValues.append(utility.streetToDoubleMetaphone(row[6]))
        #Current City Abbrev
        insertValues.append(utility.abbrevSentence(row[7]))
        #Current City DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[7]))
        #Previous First Name DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[10]))
        #Previous True MI
        insertValues.append(utility.abbrevWord(row[11]))
        #Previous MI DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[11]))
        #Previous Last Name DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[12]))
        #Previous Street 1 DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[13]))
        #Previous Street 2 DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[14]))
        #Previous City Abbrev
        insertValues.append(utility.abbrevSentence(row[15]))
        #Previous City DMeta
        insertValues.append(utility.streetToDoubleMetaphone(row[16]))
        #append patientID because we forgot
        insertValues.append(patientID)
        print(insertValues)
        formatted = "'" + "', '".join(insertValues) + "'"
        INSERT['insertData'] = (
            "INSERT INTO AdaptedData "
            "VALUES (" + formatted + ");"
        )
        cursor.execute(INSERT['insertData'])
    cnx.commit()
    cursor.close()
    cnx.close()


def calculatePatientAcctNumConfidence(patientAcctNum1, patientAcctNum2):
    if patientAcctNum1 == "" or patientAcctNum2 == "":
        return 0
    distance = utility.levenshtein(patientAcctNum1, patientAcctNum2)
    confidence = 1/pow(distance+1,0.15*distance)
    return confidence

def calculateFullNameConfidence(first1, first1DM, last1, last1DM, first2, first2DM, last2, last2DM):
    if (first1 == '' or first2 == '') and (last1 != '' or last2 != ''):
        return calculateNameConfidence(last1, last1DM, last2, last2DM)
    elif (first1 != '' or first2 != '') and (last1 == '' or last2 == ''):
        return calculateNameConfidence(first1, first1DM, first2, first2DM)
    elif ((first1 == '' or first2 == '') and (last1 == '' or last2 == '')):
        return None
    else:
        total = 0
        if utility.compareFirstLastSwap(first1, last1, first2, last2):
            total += 0.2
        total += calculateNameConfidence(first1, first1DM, first2, first2DM) * 0.3
        total += calculateNameConfidence(last1, last1DM, last2, last2DM) * 0.5
        return total

def calculateNameConfidence(name1, name1DM, name2, name2DM):
    total = 0

    # if utility.compareByAbbrevWord(name1, name2):
    #     total += 0.1
    
    # if utility.compareWordsWithoutSpecialChars(name1, name2):
    #     return 1

    # if utility.compareNameByNickname(name1, name2):
    #     total += 0.35

    if name1 == name2:
        return 1
    
    if utility.compareByContains(name1, name2):
        total += 0.2
    
    if utility.compareDoubleMetaphones(name1DM, name2DM):
        total += 0.4

    # if utility.compareByVisuallySimilarChars(name1, name2):
    #     return 1
    
    #CHANGE
    # manhattandistance = utility.compareWordsByKeyboardDistance(name1, name2)

    levDistance = utility.levenshtein(name1, name2)
    levConfidence = 1/(pow(levDistance+1,0.9*levDistance)) * 0.4
    total += levConfidence
    return total

def calculateMiddleIConfidence(middle1, middle1AB, middle1DM, middle2, middle2AB, middle2DM):
    if middle1 == "" or middle2 == "":
        return None
    total = 0

    if middle1 == middle2:
        return 1

    if middle1AB == middle2 or middle2AB == middle1:
        total += 0.15
    
    # if utility.compareWordsWithoutSpecialChars(middle1, middle2):
    #     return 1

    # if utility.compareNameByNickname(middle1, middle2):
    #     total += 0.35
    
    if utility.compareByContains(middle1, middle2):
        total += 0.15
    
    if utility.compareDoubleMetaphones(middle1DM, middle2DM):
        total += 0.35

    # if utility.compareByVisuallySimilarChars(middle1, middle2):
    #     return 1
    
    #change
    # manhattandistance = utility.compareWordsByKeyboardDistance(middle1, middle2)

    levDistance = utility.levenshtein(middle1, middle2)
    levConfidence = 1/(pow(levDistance+1,0.2*levDistance)) * .35
    total += levConfidence
    return total

def calculateDOBConfidence(dob1, dob2):
    if dob1 == "" or dob2 == "":
        return None
    if dob1 == dob2:
        return 1
    distance = utility.levenshtein(dob1, dob2)
    confidence = 1/pow(distance+1,0.5*distance)
    return confidence

def calculateSexConfidence(sex1, sex2):
    if sex1 == "" or sex2 == "":
        return None
    # try:
    #     sex1 = dictionaries.sex[sex1]
    # except KeyError:
    #     pass
    # try:
    #     sex2 = dictionaries.sex[sex2]
    # except KeyError:
    #     pass
    if sex1 == sex2:
        return 1
    if len(sex1) != len(sex2):
        return 0
    distance = utility.levenshtein(sex1, sex2)
    confidence = 1/(pow(distance+1, distance))
    return confidence

def calculateStreetConfidence(street1, street1DM, street2, street2DM):
    if street1 == "" or street2 == "":
        return None
    # street1 = street1.split(' ')
    # street2 = street2.split(' ')

    #convert street abbreviations to fully spelled out
    # try:
    #     street1[-1] = dictionaries.streets[street1[-1]]
    # except KeyError:
    #     pass
    # try: 
    #      street2[-1] = dictionaries.streets[street2[-1]]
    # except KeyError:
    #     pass
    
    if street1 == street2:
        return 1
    total = 0
    if utility.compareSentDoubleMetaphones(street1DM, street2DM):
            total += 0.5
    #double metaphone for each word
   
    # street1 = ' '.join(str(elem) for elem in street1)
    # street2 = ' '.join(str(elem) for elem in street2)

    #levenshtein
    distance = utility.levenshtein(street1, street2)
    total += 1/(pow(distance+1,0.2*distance)) * 0.5

    return total

def calculateCityConfidence(city1, city1AB, city1DM, city2, city2AB, city2DM):
    if city1 == "" or city2 == "":
        return None
    #calculate two fully spelled out cities
    #levenshtein
    else:
        total = 0
        if city1 == city2:
            return 1
        distance = utility.levenshtein(city1, city2)
        levConfidence = 1/(pow(distance+1, distance+1)) * 0.3

    #double metaphone
        if utility.compareSentDoubleMetaphones(city1DM, city2DM):
            total += 0.5

    #calculate abbreviations
        # abbreviationScore = 0
        # shortenedScore = 0
        # if utility.compareByAbbrevSentence(city1, city2):
        #     abbreviationScore = (min(len(city1),len(city2)))/5
    #calculate shortened versions (if abbreviated skip)
        if city1 == city2AB or city1AB == city2:
            total += 0.1
        if utility.compareByContains(city1,city2):
            total += 0.1
        return total

#typos on abbreviations really screw this up   
def calculateStateConfidence(state1, state2):
    #convert abbreviations to full states
    if state1 == "" or state2 == "":
        return None
    else:
        # try: 
        #     state1 = dictionaries.states[state1]
        # except KeyError:
        #     pass
        # try:
        #     state2 = dictionaries.states[state2]
        # except KeyError:
        #     pass
        if state1 == state2:
            return 1
        distance = utility.levenshtein(state1, state2)
        confidence = 1/(distance+1)
        return confidence

def calculateZipConfidence(zip1, zip2):
    if zip1 == "" or zip2 == "":
        return None
    else:
        if zip1 == zip2:
            return 1
        distance = utility.levenshtein(zip1, zip2) 
    # distance -> confidence
    #0 -> 1
    #1 -> 0.5
    #2 -> 0.11
    #3 -> .0156
        confidence = 1/(pow(distance+1, distance))
        return confidence


def getConfidenceScore(row1, row2):
    # row1 = [x.lower() for x in row1]
    # row2 = [x.lower() for x in row2]
    # row1 = [x.strip() for x in row1]
    # row2 = [x.strip() for x in row2]

    #print(row1)
    #print(row2)
    PAN_WEIGHT = 0.01
    CN_WEIGHT = 0.075
    CMI_WEIGHT = 0.01
    DOB_WEIGHT = 0.02
    S_WEIGHT = 0.04
    CS1_WEIGHT = 0.2
    CS2_WEIGHT = 0.01
    CC_WEIGHT = 0.07
    CS_WEIGHT = 0.07
    CZ_WEIGHT = 0.03
    PN_WEIGHT = 0.075
    PMI_WEIGHT = 0.01
    PS1_WEIGHT = 0.2
    PS2_WEIGHT = 0.01
    PC_WEIGHT = 0.07
    PS_WEIGHT = 0.07
    PZ_WEIGHT = 0.03


    #use dictionary in case their columns are messed up

    PAN = calculatePatientAcctNumConfidence(row1[0], row2[0])
    CN = calculateFullNameConfidence(row1[1], row1[19], row1[3], row1[22], row2[1], row2[19], row2[3], row2[22])
    CMI = calculateMiddleIConfidence(row1[2], row1[20], row1[21], row2[2], row2[20], row2[21])
    DOB = calculateDOBConfidence(row1[4], row2[4])
    S = calculateSexConfidence(row1[5], row2[5])
    CS1 = calculateStreetConfidence(row1[6], row1[23], row2[6], row2[23]) 
    CS2 = calculateStreetConfidence(row1[7], row1[24], row2[7], row2[24])
    CC = calculateCityConfidence(row1[8], row1[25], row1[26], row2[8], row2[25], row2[26])
    CS = calculateStateConfidence(row1[9], row2[9])
    CZ = calculateZipConfidence(row1[10], row2[10])

    PN = calculateFullNameConfidence(row1[11], row1[27], row1[13], row1[30], row2[11], row2[27], row2[13], row2[30])
    PMI = calculateMiddleIConfidence(row1[12], row1[28], row1[29], row2[12], row2[28], row2[29])
    PS1 = calculateStreetConfidence(row1[14], row1[31], row2[14], row2[31])
    PS2 = calculateStreetConfidence(row1[15], row1[32], row2[15], row2[32])
    PC = calculateCityConfidence(row1[16], row1[33], row1[34], row2[16], row2[33], row2[34])
    PS = calculateStateConfidence(row1[17], row2[17])
    PZ = calculateZipConfidence(row1[18], row2[18])

    confidenceScores = [PAN,CN,CMI,DOB,S,CS1,CS2,CC,CS,CZ,PN,PMI,PS1,PS2,PC,PS,PZ]
    weights = [PAN_WEIGHT,CN_WEIGHT,CMI_WEIGHT,DOB_WEIGHT,S_WEIGHT,CS1_WEIGHT,CS2_WEIGHT,CC_WEIGHT,CS_WEIGHT,CZ_WEIGHT,
                PN_WEIGHT,PMI_WEIGHT,PS1_WEIGHT,PS2_WEIGHT,PC_WEIGHT,PS_WEIGHT,PZ_WEIGHT]
    newFactor = 0
    
    for score,weight in zip(confidenceScores, weights):
        if score is not None:
            newFactor += weight

    if newFactor == 0:
        newFactor = 1

    count = 0
    newConfidenceScores = []
    for score,weight in zip(confidenceScores, weights):
        if score is None:
            newConfidenceScores.append(0)
        else:
            newConfidenceScores.append(score * weight/newFactor)
    
    score = 0
    for s in newConfidenceScores:
        score += s

    #print("Total confidence: " + str(score))
    return score

def groupByConfidenceScore(connect, confidenceThreshold):
    cursor = connect.cursor()
    retTable = {}
    retTable = (
    "ALTER TABLE Data ADD GroupID2 varchar(30);"
    )
    cursor.execute(retTable)
    alreadyAddedList = []
    groupCount = 0
    cursor.execute('SELECT PatientID FROM `Data` ORDER BY PatientID DESC LIMIT 1')
    count = cursor.fetchone()[0]
    for i in range(1,count+1):
        cursor.execute("SELECT * from `AdaptedData` WHERE PatientID=" + str(i))
        row1 = cursor.fetchone()
        if row1 in alreadyAddedList:
            continue
        cursor.execute('UPDATE Data SET GroupID2=' + str(groupCount) + ' WHERE PatientID=' + str(i))
        alreadyAddedList.append(row1)
        for j in range(1,count+1):
            cursor.execute("SELECT * from `AdaptedData` WHERE PatientID=" + str(j))
            row2 = cursor.fetchone()
            if row2 not in alreadyAddedList:
                if getConfidenceScore(row1, row2) >= confidenceThreshold:
                    cursor.execute('UPDATE Data SET GroupID2=' + str(groupCount) + ' WHERE PatientID=' + str(j))
                    alreadyAddedList.append(row2)
        groupCount += 1




'''
STRINGS
Soundex vs metaphone
Levenstein distance
Abrevations for States


Account Number: check for name in account number (feel like this is useless)
Names: abreviations, common shorter versions, soundex, levenstein, make all lowercase when checking
        common longer versions (also try to deal with anne-marie vs anne), common other spellings, keyboard distance typos, characters that look similiar
        switch first/last, special characters (T-J vs T.J vs TJ)
Date of Birth: Levenstein, swapping month/day/year, spelled out date?
Sex: abbreviations
Streets: possibly swapping of words, (do everything as names but for multiple words)
Zip: Levenstein
States: (same as names) - almost

General Notes:
lonber the word/input = more weight in confidence (because more chance to get it right)
a/o l/i m/n for physical writing forms
levenshtein or mederau/levenshtein

Street > State > City > Zip > Sex 

How to sort/compare people:
    add streets into a set (unique)
    go through the set for that street to 
'''