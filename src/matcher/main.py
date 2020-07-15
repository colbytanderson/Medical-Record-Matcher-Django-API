import algorithm
import sys
import mysql.connector
from mysql.connector import errorcode
#how do we know their table name
def main():
    args = []
    for arg in sys.argv:
        args.append(arg)
    '''
    if len(args) != 2:
        print("Invalid Arguments")
        print("Usage: python main.py <path-to-mysql database>")
        exit()
    '''
    try:
        cnx = mysql.connector.connect(user='sql3329916', password='APzc3QtGkq',
                                host='sql3.freemysqlhosting.net',
                                database='sql3329916')
        cursor = cnx.cursor()
    except:
        print("Error")
        exit()
    algorithm.start()
    algorithm.groupByConfidenceScore(cnx,0.8)

if __name__ == "__main__":
    main()