import csv
import mysql.connector
from mysql.connector import errorcode

if __name__ == "__main__":
    data = []
    with open("Patient Matching Data.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    '''
    cnx = mysql.connector.connect(user='mVlV7hcyfk', password='SXunDqvhY5',
                                host='remotemysql.com',
                                database='mVlV7hcyfk')
    '''
    cnx = mysql.connector.connect(user='sql3329916', password='APzc3QtGkq',
                                host='sql3.freemysqlhosting.net',
                                database='sql3329916')
    cursor = cnx.cursor()
    DB_NAME = "sql3329916"

    TABLE = {}

    TABLE['Test'] = (
        "CREATE TABLE IF NOT EXISTS `Data` ("
        "  `GroupID` int NOT NULL,"
        "  `PatientID` int NOT NULL,"
        "  `Patient Acct #` varchar(30) NOT NULL,"
        "  `First Name` varchar(30) NOT NULL,"
        "  `MI` varchar(10) DEFAULT NULL,"
        "  `Last Name` varchar(30) NOT NULL,"
        "  `Date of Birth` varchar(15) NOT NULL,"
        "  `Sex` varchar(10) NOT NULL, "
        "  `Current Street 1` varchar(50) NOT NULL,"
        "  `Current Street 2` varchar(50) NOT NULL,"
        "  `Current City` varchar(30) NOT NULL,"
        "  `Current State` varchar(30) NOT NULL,"
        "  `Current Zipcode` varchar(10) NOT NULL,"
        "  `Previous First Name` varchar(30) NOT NULL,"
        "  `Previous MI` varchar(10) NOT NULL,"
        "  `Previous Last Name` varchar(30) NOT NULL,"
        "  `Previous Street 1` varchar(50) NOT NULL,"
        "  `Previous Street 2` varchar(50) NOT NULL,"
        "  `Previous City` varchar(30) NOT NULL,"
        "  `Previous State` varchar(30) NOT NULL,"
        "  `Previous Zipcode` varchar(10) NOT NULL)"
    )

    try:
        cursor.execute(TABLE['Test'])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
        else: 
            print(err.msg)
    else:
        print("OK")

    for i in range(len(data)):
        if (i == 0):
            continue
        values = "'" + "', '".join(data[i]) + "'"
        insert_into_table = (
        "INSERT INTO Data " 
        "VALUES (" + values + ");"
        )
        #print(insert_into_table)
        cursor.execute(insert_into_table)
    
    cnx.commit()
    cursor.close()
    cnx.close()