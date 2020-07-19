import algorithm
import csv

#Change if necessary
FILE_NAME = "Patient Matching Data.csv"

if __name__ == "__main__": 
    data = []
    with open(FILE_NAME) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

    data = data[1:-1]
    #Returns array of groups where each group is an array of matching patients 
    result = algorithm.groupByConfidenceScore(data,0.68)

    #Output formatted as <Our Group#>:<PatientID>
    print('Printing by ID')
    counter = 1
    for groups in result:
        for patient in groups:
            print("Group" + str(counter) + ": " + patient[1])
        counter += 1

    print("---------------")
    print('Printing by categorization')
    #easier to see groups
    #formatted as <Our Group#>:<True Group Number>
    #actual values of numbers don't matter, just the categorization
    counter = 1
    for groups in result:
        for patient in groups:
            print("Group" + str(counter) + ": " + patient[0])
        counter += 1