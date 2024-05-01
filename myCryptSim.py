
# Binance Trading Methods

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
import json

errorDelim = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
buyDelim =   "/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/"
sellDelim =  "\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\"
startDelim = ".--.--.--.--.--.--.--.--.--.--.--.--.--"

def setupClient():

    #NewKey used for sim and data collection
    # Old keys
    #api_key = "fygWtUieftT2UIzOwYzsLFXDcC4AoNeA3Ph4svkyaW4zLezSoAFZmWSEXblIJRZv"
    #api_secret = "90MHSDFnBobQ3vXrIprv8yZ6i6HLQ6NjAyweW4MeuVY0flz9usDwmPl9H5ylSx7x"
    
    api_key = "uilQAa7Kj5q59yQISVVNJr0C5D1ww7iz3438wwKkFS7UoTRsrOZXBV3t7YE9gX1u"
    api_secret = "trwsBz0GcrWSxDbalJt9IC0P30xFg38c1U8dhoupcVJ0INJ5ubUwSfOKoE6Kf6yM"
    return Client(api_key, api_secret)

def setupClientCollector():
    
    api_key = "uilQAa7Kj5q59yQISVVNJr0C5D1ww7iz3438wwKkFS7UoTRsrOZXBV3t7YE9gX1u"
    api_secret = "trwsBz0GcrWSxDbalJt9IC0P30xFg38c1U8dhoupcVJ0INJ5ubUwSfOKoE6Kf6yM"
    
    return Client(api_key, api_secret)

def getCurrencyNames(client):
    marginData = client.get_margin_account()
    currency_names = []
    for x in marginData['userAssets']:
        currency_names.append(x['asset']+"USDT")
    return currency_names

def refreshCurrencyNames(client, tfName):
    marginData = client.get_margin_account()
    tf = open(tfName, 'w')
    for x in marginData['userAssets']:
        tf.write(x['asset']+"USDT\n")
    tf.close()

def getFileCurrencyNames(tfName):
    currency_names = []
    lines_array = []
    
    with open(tfName, 'r') as file:
        # Read lines and append them to the array
        lines_array = file.readlines()

    # Print the array of lines
    for line in lines_array:
        currency_names.append(line.strip())

    return currency_names

def refreshCurrencyInformation(client, currencies, tfName):
    arr = []
    with open(tfName, 'w') as file:
        for x in currencies:
            arr.append(client.get_symbol_info(x))
        json.dump(arr, file, indent=2)
    print("Currency Data Refresh Complete: ✅")
    #print("dpne with:", x)
    #print("Data extraction complete")


def read_dictionary_from_file(tfName):
    """
    Reads a dictionary with internal dictionaries from a text file in JSON format.

    Parameters:
    - file_path: Path to the text file.

    Returns:
    - The dictionary read from the file.
    """
    with open(file_path, 'r') as file:
        dictionary = json.load(file)
    return dictionary
    
    

def getPriceChange(df_data, cNames):
    #print("currency names are ",currencyNames)
    df_dif = pd.DataFrame(columns = cNames)
    #print("current df_change is: \n", df_change)
    #print("BTCUSDT max is :",(df_data["BTCUSDT"].max(axis = 0, numeric_only=False)))
    items = []
    for col in cNames:
        items.append((((float(df_data[col].values[-1]))-(float(df_data[col].values[0])))/(float(df_data[col].values[0])))*100)

    df_dif.loc[len(df_dif)] = items
    '''
    print("Incoming Price change:")
    print("----------------------------------------------")
    print(df_dif)
    print("----------------------------------------------")
    '''
    return df_dif

def getTopChangers(df_data, no):
    df_sortChange = df_data.sort_values(by = 0, axis = 1, ascending = False)
    growers = list(df_sortChange.columns)[:no]
    growersval = list(df_sortChange.values[-1:])[0][:no]
    '''
    print("Incoming Sorted Price Change")
    print("----------------------------------------------")
    print(growers)
    print(growersval)
    print("----------------------------------------------")
    '''
    return [growers, growersval]

def createMarginOcoSell(client, curSymbol, curPrice, curQuant, takeProfitPerc, stopLossPerc, unBorrowedQty, tfName, curInfo):
    '''
    Assumes total currency value is always sold
    '''
    try:
        tfLog = open(tfName, "a")
        
        #info = client.get_symbol_info(curSymbol)
        precisionPrice = 8
        precisionQuant = 8
        for x in curInfo[curSymbol]["filters"]:
            if(x["filterType"] == "PRICE_FILTER"):
                precisionPrice = x["tickSize"].find('1')-x["tickSize"].find(".")
                #print("Found PrecisionPrice Sell!!!,", precisionPrice)
            if(x["filterType"] == "LOT_SIZE"):
                precisionQuant = x["stepSize"].find('1')-x["stepSize"].find(".")
                #print("Found PrecisionQuant Sell!!!,", precisionQuant)

        sellPrice = round(curPrice*(1+(takeProfitPerc/100)), precisionPrice)
        sellPriceTrig = round(curPrice*(1-(stopLossPerc/100)), precisionPrice)
        sellPriceSL = round(curPrice*(1-(stopLossPerc+0.05)/100), precisionPrice)
        #print("Sell total Quant:", curQuant)

        tax = curQuant*0.0025
        simOrders = [{'symbol' : curSymbol, "transactTime" : datetime.now(), "buy_price" : curPrice, "OrgQty" : curQuant, "type" : "STOP_LOSS_LIMIT", "side" : "SELL",
                      "sellPriceSL" : sellPriceSL, "sellPriceTrig" : sellPriceTrig, "tax" : tax, "unBorrowedQty" : unBorrowedQty},
                     {'symbol' : curSymbol, "transactTime" : datetime.now(), "sellPrice" : sellPrice, "OrgQty" : curQuant, "executedQty" : curQuant, "type" : "LIMIT_MAKER",
                      "type" : "SELL", "unBorrowedQty" : unBorrowedQty}]
        
        tfLog.write("\n"+sellDelim)
        tfLog.write("\nSell Order Created:\n" + str(simOrders))
        tfLog.write("\n"+sellDelim)
        tfLog.close()
        #print("SimOrders are", simOrders)
        return simOrders
                    


    except Exception as e:
            # error handling goes here
            tfLog = open(tfName, "a")
            tfLog.write("\n" + errorDelim)
            tfLog.write("\nError - " + str(e))
            tfLog.write("\n" + errorDelim)
            tfLog.close()
            print(e)

def createMarginOrder(client, curSymbol, curPrice, priceBuffer, curPerc, curFree, curMarg, tfName, curInfo): #Convert to OCO order, and allow for side effect to borrow money
    '''
    Create a Margin order: (curSymbol, curPrice, curQuantity, priceBuffer)
    Assumes Margin x3 will always work until bankrupt
    '''
    try:
        tfLog = open(tfName, "a")
        info = client.get_symbol_info(curSymbol)
        precisionPrice = 8
        precisionQuant = 8
        for x in curInfo[curSymbol]["filters"]:
            if(x["filterType"] == "PRICE_FILTER"):
                precisionPrice = x["tickSize"].find('1')-x["tickSize"].find(".")
                #print("Found PrecisionPrice!!!", precisionPrice)
            if(x["filterType"] == "LOT_SIZE"):
                precisionQuant = x["stepSize"].find('1')-x["stepSize"].find(".")
                #print("Found PrecisionQuant!!!", precisionQuant)
                
        #Get the correct price and quantity precision    
        buyPrice = round(curPrice*(1+(priceBuffer/100)), precisionPrice)
        buyQuant = math.floor((curFree/curPrice) * 0.99 * (curPerc/100) * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
        buyQuantx3 = math.floor((curFree/curPrice) * 0.99 * 3 * (curPerc/100) * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
        buyQuantx2 = math.floor((curFree/curPrice) * 0.99 * 2 * (curPerc/100) * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
        

        totalQuant = buyQuant*1
        #print("Initial buyQuant =", buyQuant)
        #print("Margin buyQuant(x3) =", buyQuantx3)
        
        #Create the margin order
        try:
            #Create margin order with x3 leverage
            simOrder = {'symbol' : curSymbol, "transactTime" : datetime.now(), "price" : curPrice, "executedQty" : buyQuantx3, "Status" : "Filled"}
            totalQuant = buyQuantx3
            #Used when no BNB is present to pay fees
            '''
            totalQuant = 0
            for x in order["fills"]:
                totalQuant += (float(x["qty"]) - float(x["commission"]))
            totalQuant = math.floor(totalQuant * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
            '''
            print("Successfully created x3 Margin Order")
            #print("TotalQuant is:", totalQuant)
            
        except Exception as e:
            try:
                tfLog.write("\n" + errorDelim)
                tfLog.write("\nx3 margin order Failed:\n" + str(e))
                tfLog.write("\n" + errorDelim)
                #Create margin order with x2 leverage
                simOrder = {'symbol' : curSymbol, "transactTime" : datetime.now(), "price" : curPrice, "executedQty" : buyQuantx2, "Status" : "Filled"}
                totalQuant = buyQuantx2
                '''
                totalQuant = 0
                for x in order["fills"]:
                    totalQuant += (float(x["qty"]) - float(x["commission"]))
                totalQuant = math.floor(totalQuant * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
                '''
                print("Successfully created x2 Margin Order")
                #print("TotalQuant is:", totalQuant)
            except Exception as e:
                tfLog.write("\n" + errorDelim)
                tfLog.write("\nx2 margin order Failed:\n" + str(e))
                tfLog.write("\n" + errorDelim)
                #Create standard margin order
                simOrder = {'symbol' : curSymbol, "transactTime" : datetime.now(), "price" : curPrice, "executedQty" : buyQuant, "Status" : "Filled"}
                '''
                totalQuant = 0
                for x in order["fills"]:
                    totalQuant += (float(x["qty"]) - float(x["commission"]))
                totalQuant = math.floor(totalQuant * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
                '''
                totalQuant = math.floor(totalQuant * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
                print("Successfully created x1 Margin Order")
                #print("TotalQuant is:", totalQuant)
                
        tfLog.write("\n"+buyDelim)
        tfLog.write("\nBuy Order Created:\n" + str(simOrder))
        tfLog.write("\n"+buyDelim)
        print("Order Successfully created in order!")

        tfLog.close()
        
        #Create Sell Order
        return createMarginOcoSell(client, curSymbol,buyPrice, totalQuant, 4, 3, buyQuant, tfName, curInfo)

        

    except Exception as e:
        tfLog = open(tfName, "a")
        tfLog.write("\n" + errorDelim)
        tfLog.write("\nError - " + str(e))
        tfLog.write("\n" + errorDelim)
        tfLog.close()
        print(e)

def tfLogStart(tfName, amt):
    tfLog = open(tfName, 'a')
    tfLog.write(startDelim)
    tfLog.write("\nOpen: " + str(datetime.now()) + "\n")
    tfLog.write("Current Amount: "+ str(amt) +" USDT\n")
    tfLog.write(startDelim+"\n")
    tfLog.close()

    
