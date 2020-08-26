import random
from random import seed
from random import randint
import csv
import argparse
from datetime import date, timedelta, datetime as dt
import threading
import sys
import json
import os
import mysql.connector
from mysql.connector import errorcode
import time

lock = threading.Lock()

volatility = 1  # .001

#arrays used to store ficticous securities
company_symbol=[]
company_name=[]

#the following two functions are used to come up with some fake stock securities
def generate_symbol(a,n,e):
    #we need to break this out into its own function to do checks to make sure we dont have duplicate symbols
    for x in range(1,len(a)):
        symbol=str(a[:x]+n[:1]+e[:1])
        if symbol not in company_symbol:
            return symbol

def generate_securities(numberofsecurities):
    with open('adjectives.txt', 'r') as f:
        adj = f.read().splitlines()
    with open('nouns.txt', 'r') as f:
        noun = f.read().splitlines()
    with open('endings.txt', 'r') as f:
        endings = f.read().splitlines()
    for i in range(0,numberofsecurities,1):
        a=adj[randint(0,len(adj)-1)].upper()
        n=noun[randint(0,len(noun))].upper()
        e=endings[randint(0,len(endings)-1)].upper()
        company_name.append(a + ' ' + n + ' ' + e)
        company_symbol.append(generate_symbol(a,n,e))

#this function is used to randomly increase/decrease the value of the stock, tweak the random.uniform line for more dramatic changes

def getvalue(old_value):
    change_percent = volatility * \
        random.uniform(0.0, .001)  # 001 - flat .01 more
    change_amount = old_value * change_percent
    if bool(random.getrandbits(1)):
        new_value = old_value + change_amount
    else:
        new_value = old_value - change_amount
    return round(new_value, 2)


def main():
    global args
    global MYSQL_CONNECTIONSTRING

    # capture parameters from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--symbols", type=int, help="number of financial stock symbols")
    parser.add_argument("-c","--connection", default='127.0.0.1', help="MySQL host string")
    parser.add_argument("-u","--username", default='mysqluser', help="MySQL username")
    parser.add_argument("-p","--password", default='pass@word1', help="MySQL password")

    args = parser.parse_args()

    if args.symbols:
        if args.symbols < 1:
            args.symbols = 1

    MYSQL_CONNECTIONSTRING = {
    'user': args.username,
    'password': args.password,
    'host': args.connection,
    'database': 'Stocks',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password'
    }

    threads = []

    generate_securities(args.symbols)

    for i in range(0, 1): # parallel threads
        t = threading.Thread(target=worker, args=[int(i), int(args.symbols)])
        threads.append(t)
    for x in threads:
        x.start()
    for y in threads:
        y.join()

#When the conainters launch, we want to not crash out if the MySQL Server container isn't fully up yet so here we wait until we can connect
def checkmysqlconnection():
    try:
        cnx = mysql.connector.connect(**MYSQL_CONNECTIONSTRING)
        time.sleep(2)
        cnx.close()
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return False
    else:
        cnx.close()
        return False
    

def worker(workerthread, numofsymbols):
    try:
        #inital security values
        last_value=[]
        for i in range(0,numofsymbols):
            last_value.append(round(random.uniform(1, 100), 2))
        
        # due to the container spinning up before the mysql container has a chance to get initialized we need to make sure we wait long enough before pounding it
        while True:
            if checkmysqlconnection()==False:
                time.sleep(10)
                print('Problem connecting to MySQL, sleeping 10 seconds')
            else:
                break

        cnx = mysql.connector.connect(**MYSQL_CONNECTIONSTRING)
        while True:
            for i in range(0,numofsymbols):
                cursor = cnx.cursor()
                x = getvalue(last_value[i])
                last_value[i] = x
                txtime = dt.now()
                addData = ("INSERT INTO StockData (company_symbol, company_name, price, tx_time) VALUES (%s, %s, %s, %s)")
                cursor.execute(addData,(company_symbol[i], company_name[i],x,txtime.strftime('%Y-%m-%d %H:%M:%S')))
                cnx.commit()
                cursor.close()
                print(company_symbol[i] + ' ' + company_name[i] + ' traded at ' + str(x) + ' ' + txtime.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(1)
        cnx.close()
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise


main()
