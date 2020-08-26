from flask import Flask
import pymongo
from pymongo import errors
import mysql.connector
from mysql.connector import errorcode
import time

app = Flask(__name__)

def checkmongodbconnection():
    try:
        c = pymongo.MongoClient(MONGO_URI)
        c.admin.command('ismaster')
        time.sleep(2)
        c.close()
        return True
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print('Could not connect to server: %s',e)
        return False
    else:
        c.close()
        return False


@app.route("/reset")
def resetme():
    c = pymongo.MongoClient("mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0")
    db = c.get_database(name='Stocks')
    mycol = db["StockData"]
    mycol.delete_many({})
    return "<B>Database reset</B>"
    
@app.route("/")
def hello():
    global MYSQL_CONNECTIONSTRING
    global MONGO_URI

    MONGO_URI="mongodb://mongo1:27017,mongo2:27018,mongo3:27019/?replicaSet=rs0"

    MYSQL_CONNECTIONSTRING = {
    'user': "mysqluser",
    'password': "pass@word1",
    'host': 'mysqlstock',
    'database': 'Stocks',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password'
    }

    while True:
        print('Checking MongoDB Connection')
        if checkmongodbconnection()==False:
            print('Problem connecting to MongoDB, sleeping 10 seconds')
            time.sleep(10)
        else:
            break
    print('Successfully connected to MongoDB')

    try:
        c = pymongo.MongoClient(MONGO_URI)
        db = c.get_database(name='Stocks')
        mycol = db["StockData"]
        stocks=mycol.aggregate([
        {
            '$group': {
                '_id': '$company_symbol', 
                'company_name': {
                    '$first': '$company_name'
                }, 
                'price': {
                    '$first': '$price'
                }, 
                'tx_time': {
                    '$first': '$tx_time'
                }
            }
        }
    ])
        x="<html><body><h1>Stock securities in MongoDB</h1><br><table>"
        for stock in stocks:
            x+='<tr><td>' + stock[u'_id']+ '</td><td>' + stock[u'company_name'] + '</td><td>' + str(stock[u'price'])+ '</td><td>' + str(stock[u'tx_time']) + '</td></tr>'
        x=x+'</table>'

    except Exception as e:
        print("mongo error: " + str(e))
    
    cnx = mysql.connector.connect(**MYSQL_CONNECTIONSTRING)
    mycursor = cnx.cursor()

    mycursor.execute("SELECT DISTINCT c.company_symbol, (SELECT DISTINCT n.company_name from StockData n where n.company_symbol=c.company_symbol) as 'company_name', (SELECT MAX(p.price) from StockData p where p.company_symbol=c.company_symbol) as 'price', (SELECT MAX(t.tx_time) from StockData t where t.company_symbol=c.company_symbol) as 'tx_time'  from StockData c LIMIT 10;")

    myresult = mycursor.fetchall()

    x+="<h1>Stock securities in MySQL</h1><br><table>"
    for stock in myresult:
           x+='<tr><td>' + str(stock[0])+ '</td><td>' + str(stock[1]) + '</td><td>' + str(stock[2])+ '</td><td>' + str(stock[3]) + '</td></tr>'
    x=x+'</table></body></html>'
    return x

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
