#!/usr/bin/python3

"""
File:  [ functions1.py ]
Author: Samuel Schatz
Date: 9/17/2020 
Description: The main bot for this project.
"""
# functions1.py
import os
import csv
import sys
import json
import time
import config
import pprint
import datetime
import pandas as pd
import mysql.connector
from datetime import date
from time import sleep as s
from datetime import datetime
from statistics import median

#import objgraph

if sys.platform == 'linux':
    import sqlite3

def openSL():
    conn = sqlite3.connect(config.linux_active_logspath + 'main.db')
    return conn

def closeSL():
    conn = openSL()
    conn.close()

def c1():
    db = mysql.connector.connect(
        host=config.DB_host,
        user='admin',
        passwd=config.DB_pass,
        database='MLDS',
        auth_plugin='mysql_native_password'
    )
    return db

def datetimeNow():
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

def counter1():
    if sys.platform == "win32":
        file1 = config.windowsCounter
    elif sys.platform == "linux":
        file1 = config.linuxCounter
    with open(file1) as f1:
        data = json.load(f1)
    f1.close()

    val = data["counter"]
    data["counter"] += 1

    with open(file1, "w") as f2:
        json.dump(data, f2, sort_keys=False, indent=1)
    f2.close()
    return val

def toJson(val):
    if sys.platform == "win32":
        path = config.windowsPath
    elif sys.platform == "linux":
        path = config.linuxPath
        checkFile = config.linuxFileLog
    
    df = pd.read_csv(checkFile)
    names = df['filename']
    entries1 = df['entries']
    dateF = df['datefilled']

    e = True
    x = 0
    while (e == True):
        if (entries1[x] == 0):
            jsonF = names[x]
            e = False
        else:
            x += 1


    jsonF = str(jsonF)
    with open(jsonF) as f:
        data = json.load(f)
    f.close()

    data["data"].append(val)
    s(0.5)
    data["counter"] += 1

    with open(jsonF, "w") as f1:
        json.dump(data, f1, sort_keys=False, indent=4)
    f1.close()

    if data['counter'] >= 180000:
        entries1[x] = 180000
        dateF[x] = datetimeNow()
        df['entries'] == entries1
        df['datefilled'] == dateF
        

    df.to_csv(checkFile, encoding='utf-8', index=False)

    #if sys.platform == "linux":
    #    toPublicJson()

def checkTime():
    tn = datetime.now()
    tn = int(tn.minute)
    if tn % 15 == 0:
        return True
    elif tn == 59:
        return True
    else:
        return False

def toChange(val):
    with open(config.non_pushlog, 'w', newline='') as f1:
        cw = csv.writer(f1)
        cw.writerow(val)
    f1.close()


def tolog(val):
    db = c1()
    cursor = db.cursor()
    statement = 'INSERT INTO raw_data(status, date) VALUES(%s,%s)'
    tup = (val[0], val[1])
    cursor.execute(statement, tup)
    db.commit()
    db.close()

    # adding a check time here so we can moniter the change closely
    if checkTime() == True:
        TL = [
            datetime.today().strftime('%H:%M:%S %Y-%m-%d'),
            int(getCount())
        ]
        toChange(TL)
    
    #objgraph.show_growth(limit=3)

def toPublicJson():
    path = "/var/www/dadywarbucks.xyz/public_html/"
    path2 = config.linuxPathlog
    f1 = "logs1.json"
    jsonF = str(path2+f1)
    jsonF2 = str(path+f1)
    with open(jsonF) as f:
        data = json.load(f)
    f.close()

    with open(jsonF2, "w") as f1:
        json.dump(data, f1, sort_keys=False, indent=4)
    f1.close()


def getCount():
    db = c1()
    cursor = db.cursor()

    cursor.execute('SELECT id FROM raw_data;')
    id1 = cursor.fetchall()
    return len(id1)
    

def writeSuggestions(data):
    if sys.platform == "win32":
        path = config.windowsPathLogs
    elif sys.platform == "linux":
        path = config.linuxPathlog

    f1 = path + "suggestions.txt"

    with open(f1, "a") as f:
        f.write(data)
    f.close()
    


def addOptOut(username):
    if sys.platform == "win32":
        file1 = config.windowsOptOut
    elif sys.platform == "linux":
        file1 = config.linuxOptOut

    with open(file1) as f:
        data = json.load(f)
    f.close()
    data["users"].append(username)
    
    with open(file1, "w") as f1:
        json.dump(data, f1, sort_keys=False, indent=4)
    f1.close()

def getOptedOut():
    if sys.platform == "win32":
        file1 = config.windowsOptOut
    elif sys.platform == "linux":
        file1 = config.linuxOptOut

    with open(file1) as f:
        data = json.load(f)
    f.close()
    return data["users"]

def regServer(SN):
    if sys.platform == "win32":
        path = config.windowsPathLogs
    elif sys.platform == "linux":
        path = config.linuxPathlog
    f1 = "servers.json"
    jsonF = str(path+f1)
    with open(jsonF) as f:
        data = json.load(f)
    f.close()

    if SN not in data["servers"]:
        data["servers"].append(SN)

        with open(jsonF, "w") as f1:
            json.dump(data, f1, sort_keys=False, indent=4)
        f1.close()
        return True
    else:
        return False

def countTEST():
    onlineT = []
    onlineH = []
    offlineT = []
    offlineH = []
    if sys.platform == "win32":
        path = config.windowsPathLogs
    elif sys.platform == "linux":
        path = config.linuxPathlog
    f1 = "logs.json"
    f2 = str(path + "processOnline.csv")
    f3 = str(path + "processOffline.csv")
    jsonF = str(path+f1)
    with open(jsonF) as f:
        data = json.load(f)
    f.close()

    x = 0
    
    while(x != len(data["data"])):
        if data["data"][x][0] == "online":
            temp = str(data["data"][x][1])
            temp2 = time.strptime(temp, '%Y-%m-%d-%H:%M:%S')
            onlineH.append(int(temp2.tm_hour))
            onlineT.append(temp2)
        elif data["data"][x][0] == "offline":
            temp = str(data["data"][x][1])
            temp2 = time.strptime(temp, '%Y-%m-%d-%H:%M:%S')
            offlineH.append(int(temp2.tm_hour))
            offlineT.append(temp2)
        x += 1

    x = 0
    with open(f2, "w") as o1:
        csvWriter1 = csv.writer(o1)
        while(x != len(onlineT)):
            csvWriter1.writerow(onlineT[x])
            x += 1
    o1.close()

    x = 0
    with open(f3, "w") as o2:
        csvWriter1 = csv.writer(o2)
        while(x != len(offlineT)):
            csvWriter1.writerow(offlineT[x])
            x += 1
    o1.close()

    return onlineH

def copy():
    if sys.platform == "win32":
        print("cant copy on windows")
    elif sys.platform == "linux":
        path = config.linuxPathlog
        path2 = "/var/www/dadywarbucks.xyz/public_html/"
        file1 = path + "ML_log.json"
        file2 = path2 + "ML_log.json"
        with open(file1) as f1:
            data = json.load(f1)
        f1.close()

        with open(file2, "w") as f1:
            json.dump(data, f1, sort_keys=False, indent=4)
        f1.close()
        #print("coppied")
    


def getHoursCount(val):
    x = 0
    medians = []
    size = len(val)

    x0 = 0  
    vals = []
    while(x0 != 24):
        vals.append(0)
        x0 += 1

    while(x != size):
        y = 0
        while(y != 24):
            if val[x] == y:
                vals[y] += 1
            y += 1
            
        x += 1
    return vals, medians

def getMedian(val):
    out = median(val)
    return out

def copyimg():
    import shutil 
    path1 = config.linuxImagePath
    path2 = "/var/www/dadywarbucks.xyz/public_html/img/"
    for file in os.listdir(path1):
        if file.endswith(".png"):
            shutil.move(path1, path2)
