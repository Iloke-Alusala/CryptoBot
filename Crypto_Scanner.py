import os
import time
import schedule
import urllib.request, json
from datetime import datetime
import pandas as pd
import keyboard
import matplotlib.pyplot as plt
import math
from binance.client import Client
from myCrypt import *
from indicatorPack1Real import *
from mailSender import *

# init
#api_key = os.environ.get('binance_api')
#api_secret = os.environ.get('binance_secret')

#Initial Setup 
#---------------------------------------

def main ():
    client = setupClient()
    data = client.get_account()
    betadata = data["balances"]
    amt = 0
    tfName = "CryptoLogging.txt"
    tfBannedName = "bannedCrypt.txt"
    lastAmtName = "lastAmt.txt"
    
    
    buyThreshold = 4

    # setup Triggers for valideSMA indicator
    trig3 = 0.035
    trigMult2 = 13
    trigMult1 = 25

    BNBRefillTrigger = 0.0001
    
    tfLastAmt = open(lastAmtName, "w")
    
    for x in betadata:
        if(x["asset"] == "USDT"):
            amt = float(x["free"])
            tfLastAmt.write(str(amt))

    prices = client.get_all_tickers()

    #createSpotOrder(client, "PROSUSDT",0.52, 0.25, 100, amt, tfName)
    
    #print(prices)
    #createOrder(client, "ORDIUSDT", 55.10, 0, 100, amt, 1, tfName)
            
    #createOrder(client, 'GFTUSDT', 0.01679, 0.25, 100, amt, 1, tfName)
    
    tfLastAmt.close()
    tfLogStart(tfName, amt)
    
    #print(client.get_open_margin_orders())

    
    #Start Logging
    #-- Format of : marginPrices -> [{'symbol': 'BTCUSDT', 'price': '29168.58000000'}, {'symbol': 'ETHUSDT', 'price': '1824.36000000'}]

    #Initialization
    #---------------------------------------

    #currency_names = getCurrencyNames(client)
    prices = client.get_all_tickers()
    timeFormat = "%H:%M:%S"
    cnt = 0
    df_cols = ["Time"]
    tfBanned = open(tfBannedName, "r")
    banned = tfBanned.read().split(", ")
    tfBanned.close()
    print("Banned Tokens:", banned)
    
    open_orders = client.get_open_orders()
    marginPrices = []
    coinPrices = {}
    #Age of data that is to be stored(minutes)
    resetDuration = 15
    sleepTime = 0
    buys = 1

    #print(marginPrices)
    #print("Getting Info: ----------- \n",client.get_symbol_info("BTCUSDT"))

    for x in marginPrices:
        df_cols.append(list(x.values())[0])
    df_coin  = pd.DataFrame(columns = df_cols)
    #print("cols is :", df_cols)
    #df that stores the change in price in the last 15 minutes
    df_data = pd.DataFrame(columns = df_cols[1:])
    startTime = datetime.now()
    dfSave = {}
    prevOrder = False
    inCur = ""
    done = True
    print("Starting Botto: 👾")
    while(done):
        prices = client.get_all_tickers()

        marginPrices = []
        coinPrices = {}
        df_cols = ["Time"]
        index = 0

        currentTime = datetime.now()

        coinPrices["Time"] = currentTime

        #ONLY CHANGE THIS TO ENSURE MONITORING OF ALL CURRENCY PAIRS ENDING IN USDT
        #filter out margin prices
        for x in prices:
            if(len(x['symbol'])>=4):
                if(x['symbol'][-4:] == "USDT"):
                    marginPrices.append(x)
                    coinPrices[x["symbol"]] = x["price"]
                    
        #get all coin names
        for x in marginPrices:
            df_cols.append(list(x.values())[0])

        #add prices to df
        df_coin = df_coin._append(coinPrices, ignore_index = True)


        #delete rows over resetDuration minutes old
        while((datetime.now() - df_coin["Time"][0]).total_seconds()/60 > resetDuration):
            df_coin.drop(labels = 0, axis = 0, inplace = True)
            df_coin = df_coin.reset_index(drop=True)

        #update price change
        df_datanew = getPriceChange(df_coin, df_cols[1:len(df_cols)])
        print("df_data is:\n",df_datanew)
        markers = getTopChangers(df_datanew, 15) # returns[growers, growersval]
        
        if(open_orders != []):
            '''
            print("Open Orders")
            print("------------------------------------")
            print("------------------------------------")
            '''
            open_orders = client.get_open_orders()
        if(open_orders==[]):
            if(prevOrder):
                newAmt = 0
                data = client.get_account()
                betadata = data["balances"]
                for x in betadata:
                    if(x["asset"] == "USDT"):
                        newAmt = float(x["free"])
                    if(x["asset"]=="BNB"):
                        if(float(x["free"]) < BNBRefillTrigger):
                            send_email("alusalailoke@gmail.com", "BOTTO BNB REFILL IMMINENT", "CRITICAL: Refill BNB Tax or bot may malfunction on next purchase")
                        
                tfAmt = open(lastAmtName, "r")
                amt = float(tfAmt.read())
                tfAmt.close()
                
                tfLog = open(tfName, "a")
                tfLog.write("\n################################")
                tfLog.write("\nSale made with " + inCur + ": \n Previous USDT:" + str(amt) + "\nNew USDT:" + str(newAmt) +"\n")
                if(newAmt >= amt):
                    tfLog.write("\nNet Profit GAIN: " + str(round(newAmt/amt*100 -100, 2)) + "%\n")
                    #May need review later
                    '''
                    banned = ["PEPEUSDT", inCur, ]
                    tfBanned = open(tfBannedName, "w")
                    tfBanned.write(inCur)
                    tfBanned.close()
                    print("Banned Tokens:", banned)
                    '''
                else:
                    tfLog.write("\nNet Profit LOSS: " + str(round(100 - newAmt/amt*100, 2)) + "%\n")
                    '''
                    tfBanned = open(tfBannedName, "r")
                    newBan = tfBanned.read()
                    tfBanned.close()
                    if(newBan != ['\n']):
                        banned.append(inCur)
                        newBan += ", "+inCur
                        tfBanned = open(tfBannedName, "w")
                        tfBanned.write(newBan)
                        tfBanned.close()
                    else:
                        banned.append(inCur)
                        tfBanned = open(tfBannedName, "w")
                        tfBanned.write(inCur)
                        tfBanned.close()
                    print("Banned Tokens:", banned)
                    '''
                tfLog.write("\n################################")
                tfLog.close()
                prevOrder = False
                amt = float(newAmt)
                tfAmt = open(lastAmtName, "w")
                tfAmt.write(str(amt))
                tfAmt.close()
                print("\nNew Amount is: ", amt,"\n")
                buys = 1
                    
            for i in range(len(markers)):
                if(not(markers[0][i] in banned)):
                    if(buys==1):
                        if((markers[1][i] >= buyThreshold) and valideSMA( trig3*trigMult1 , trig3*trigMult2, trig3, 0.011, 0.011, 0.011, 1, 5, 240, markers[0][i],
                                                                          (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))):
                            data = client.get_account()
                            for x in data['balances']:
                                if(x['asset']=="USDT"):
                                    amt = float(x['free'])
                            open_orders = [createSpotOrder(client, markers[0][i], float(df_coin[markers[0][i]].values[-1:][0]), 0.25, 100, amt, tfName)]
                            inCur = markers[0][i]
                            prevOrder = True
                            buys = 0
                            pass
        else:
            buys=0
        cnt += 1
        dfSave = df_coin
        #print(marginPrices)
        time.sleep(sleepTime)


if __name__ == "__main__":
    #allow for restart after exception thrown
    while(True):
        try:
            main()
        except Exception as e:
            print(e)
            tfLog = open("CryptoLogging.txt", "a")
            tfLog.write("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            tfLog.write("\nError - " + str(e))
            tfLog.write("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            tfLog.close()
            pass
    '''
    client = setupClient()
    data = client.get_margin_account()
    betadata = data["userAssets"]
    amt = 0
    tfName = "CryptoLogging.txt"
    tfBannedName = "bannedCrypt.txt"
    lastAmtName = "lastAmt.txt"
    for x in betadata:
        if(x["asset"] == "USDT"):
            amt = float(x["free"])
    print(data)
    print(betadata)
    createMarginOrder(client, "OAXUSDT", 0.1502, 0.25, 100, amt, 0, tfName)
    '''
