from .import algorithm
import csv

def removeHeaderFromCSVAndRead(csvFile):
    data = []
    reader = csv.reader(csvFile)
    for row in reader:
        data.append(row)

    return data[1:-1]

def formatReturn(result):
    retDict = {}
    counter = 1
    for groups in result:
        for patient in groups:
            retDict[patient[1]] = "Group" + str(counter)
        counter += 1
    return retDict

# columns is queryset
def main(file, columns, recordConfidenceScore, fullNameConfidenceScore=0.1):
    data = removeHeaderFromCSVAndRead(file)
    result = algorithm.groupByConfidenceScore(data, columns, recordConfidenceScore, fullNameConfidenceScore)
    return formatReturn(result)


# overallConfidenceScore = 0.68
# PAN_WEIGHT = 0.01
# CN_WEIGHT = 0.1
# CMI_WEIGHT = 0.01
# DOB_WEIGHT = 0.06
# S_WEIGHT = 0.04
# CS1_WEIGHT = 0.2
# CS2_WEIGHT = 0.01
# CC_WEIGHT = 0.07
# CS_WEIGHT = 0.07
# CZ_WEIGHT = 0.03
# PN_WEIGHT = 0.05
# PMI_WEIGHT = 0.01
# PS1_WEIGHT = 0.16
# PS2_WEIGHT = 0.01
# PC_WEIGHT = 0.07
# PS_WEIGHT = 0.07
# PZ_WEIGHT = 0.03
    
    # skip 0 and 1
# PAN = calculatePatientAcctNumConfidence(row1[2], row2[2])
    # CN = calculateFullNameConfidence(row1[3], row1[5], row2[3], row2[5])
    # CMI = calculateMiddleIConfidence(row1[4], row2[4])
    # DOB = calculateDOBConfidence(row1[6], row2[6])
    # S = calculateSexConfidence(row1[7], row2[7]) 
    # CS1 = calculateStreetConfidence(row1[8], row2[8]) 
    # CS2 = calculateStreetConfidence(row1[9], row2[9])
    # CC = calculateCityConfidence(row1[10], row2[10])
    # CS = calculateStateConfidence(row1[11], row2[11])
    # CZ = calculateZipConfidence(row1[12], row2[12])

    # PN = calculateFullNameConfidence(row1[13], row1[15], row2[13], row2[15])
    # PMI = calculateMiddleIConfidence(row1[14], row2[14])
    # PS1 = calculateStreetConfidence(row1[16], row2[16])
    # PS2 = calculateStreetConfidence(row1[17], row2[17])
    # PC = calculateCityConfidence(row1[18], row2[18])
    # PS = calculateStateConfidence(row1[19], row2[19])
    # PZ = calculateZipConfidence(row1[20], row2[20])

    # confidenceScores = [PAN,CN,CMI,DOB,S,CS1,CS2,CC,CS,CZ,PN,PMI,PS1,PS2,PC,PS,PZ]
    # weights = [PAN_WEIGHT,CN_WEIGHT,CMI_WEIGHT,DOB_WEIGHT,S_WEIGHT,CS1_WEIGHT,CS2_WEIGHT,CC_WEIGHT,CS_WEIGHT,CZ_WEIGHT,
                # PN_WEIGHT,PMI_WEIGHT,PS1_WEIGHT,PS2_WEIGHT,PC_WEIGHT,PS_WEIGHT,PZ_WEIGHT]
