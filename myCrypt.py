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

errorDelim = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
buyDelim =   "/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/"
sellDelim =  "\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\"
startDelim = ".--.--.--.--.--.--.--.--.--.--.--.--.--"

def setupClient():
    api_key = "Enter API Key"
    api_secret = "Enter Secret Key"

    return Client(api_key, api_secret)

def getCurrencyNames(client):
    marginData = client.get_margin_account()
    currency_names = []
    for x in marginData['userAssets']:
        currency_names.append(x['asset']+"USDT")
    return currency_names

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

def createMarginOcoSell(client, curSymbol, curPrice, curQuant, takeProfitPerc, stopLossPerc, tfName):
    try:
        tfLog = open(tfName, "a")
        info = client.get_symbol_info(curSymbol)
        precisionPrice = 8
        precisionQuant = 8
        for x in info["filters"]:
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
            
        order = client.create_margin_oco_order(
            symbol=curSymbol,
            side = "SELL", #Side is either 'BUY' or 'SELL'
            quantity = curQuant,
            price = sellPrice,                                                                                                                                               
            stopPrice = sellPriceTrig,
            stopLimitPrice = sellPriceSL,
            stopLimitTimeInForce='GTC',
            sideEffectType = "AUTO_REPAY")
        
        tfLog.write("\n"+sellDelim)
        tfLog.write("\nSell Order Created:\n" + str(order))
        tfLog.write("\n"+sellDelim)
        tfLog.close()


    except Exception as e:
            # error handling goes here
            tfLog = open(tfName, "a")
            tfLog.write("\n" + errorDelim)
            tfLog.write("\nError - " + str(e))
            tfLog.write("\n" + errorDelim)
            tfLog.close()
            print(e)

def createMarginOrder(client, curSymbol, curPrice, priceBuffer, curPerc, curFree, curMarg, tfName): #Convert to OCO order, and allow for side effect to borrow money
    '''
    Create a Margin order: (curSymbol, curPrice, curQuantity, priceBuffer)
    '''
    try:
        tfLog = open(tfName, "a")
        info = client.get_symbol_info(curSymbol)
        precisionPrice = 8
        precisionQuant = 8
        for x in info["filters"]:
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
            order = client.create_margin_order(
                symbol = curSymbol,
                side = "BUY",
                quantity = buyQuantx3,
                type="LIMIT",
                TimeInForce='GTC',
                sideEffectType="MARGIN_BUY",
                price = buyPrice)
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
                order = client.create_margin_order(
                    symbol = curSymbol,
                    side = "BUY",
                    quantity = buyQuantx2,
                    type="LIMIT",
                    TimeInForce='GTC',
                    sideEffectType="MARGIN_BUY",
                    price = buyPrice)
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
                order = client.create_margin_order(
                    symbol = curSymbol,
                    side = "BUY",
                    quantity = buyQuant,
                    type="LIMIT",
                    TimeInForce='GTC',
                    sideEffectType="MARGIN_BUY",
                    price = buyPrice)
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
        tfLog.write("\nBuy Order Created:\n" + str(order))
        tfLog.write("\n"+buyDelim)
        #print("Order Successfully created in order!")
        #print(client.get_open_margin_orders())

        complete = False
        while(not(complete)):
            openOrders = client.get_open_margin_orders()
            #print("Open orders \n -------------- \n,", openOrders,"-------------- \n")
            if(openOrders == []):
                complete = True
        
        #Loan remaining amount available: UPDATE -> Loan does not work the same as borowwing
        '''
        try:
            #--------_#######--------
            complete = True

            if(curMarg > 1):     
                print("Trying now to get loan")
                print("curSymbol :", curSymbol[:-4],"\n amount :", str(round(buyQuant*(curMarg-1), precisionQuant)))
                #transaction = client.create_margin_loan(asset=curSymbol[:-4], amount=str(round(buyQuant*(curMarg-1.1), precisionQuant)))
                totalQuant = math.floor(buyQuant*(curMarg-1) + round((curFree/curPrice) * 0.98 * (curPerc/100)) * (10**precisionQuant))/(10**precisionQuant)
                print("Loan successfully created!!!!!!!!")
                tfLog.write("\n------------------------------")
                tfLog.write("\nLoan successfuly taken:\n" + str(transaction))
                tfLog.write("\n------------------------------")
            print("successfully created sell order")

        except Exception as e:
            tfLog.write("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            tfLog.write("\nLoan unsuccessfuly taken:\n" + str(e))
            tfLog.write("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            print("Loan Failed")
            totalQuant = int(buyQuant)
        '''
        tfLog.close()
        
        #Create Sell Order
        createMarginOcoSell(client, curSymbol,curPrice, totalQuant, 5, 10, tfName)

        

    except Exception as e:
        tfLog = open(tfName, "a")
        tfLog.write("\n" + errorDelim)
        tfLog.write("\nError - " + str(e))
        tfLog.write("\n" + errorDelim)
        tfLog.close()
        print(e)

def createSpotOrder(client, curSymbol, curPrice, priceBuffer, curPerc, curFree, tfName): #Convert to OCO order, and allow for side effect to borrow money
    '''
    Create a Margin order: (curSymbol, curPrice, curQuantity, priceBuffer)
    Assumes Margin x3 will always work until bankrupt
    '''
    try:
        tfLog = open(tfName, "a")
        info = client.get_symbol_info(curSymbol)
        print(info)
        precisionPrice = 8
        precisionQuant = 8
        for x in info['filters']:
            if(x["filterType"] == "PRICE_FILTER"):
                precisionPrice = x["tickSize"].find('1')-x["tickSize"].find(".")
                print("Found PrecisionPrice!!!", precisionPrice)
            if(x["filterType"] == "LOT_SIZE"):
                precisionQuant = x["stepSize"].find('1')-x["stepSize"].find(".")
                print("Found PrecisionQuant!!!", precisionQuant)

        #Get the correct price and quantity precision    
        buyPrice = round(curPrice*(1+(priceBuffer/100)), int(precisionPrice))
        buyQuant = math.floor((curFree/curPrice) * 0.95 * (curPerc/100) * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))


        totalQuant = buyQuant*1
        print("Initial buyQuant =", buyQuant)

        order = {}
        #Create the order
        try:
            #Create Spot order
            order = client.create_order(
                symbol = curSymbol,
                side = "BUY",
                type = "MARKET",
                quantity = buyQuant,
                price = buyPrice)
            #Used when no BNB is present to pay fees
            '''
            totalQuant = 0
            for x in order["fills"]:
                totalQuant += (float(x["qty"]) - float(x["commission"]))
            totalQuant = math.floor(totalQuant * (10**max(0,precisionQuant))) /(10**max(0,precisionQuant))
            '''
            print("Successfully created SPOT Order")
            #print("TotalQuant is:", totalQuant)

        except Exception as e:
                print("EXCEPTION:\n", e)
                tfLog.write("\n" + errorDelim)
                tfLog.write("\nSPOT order Failed:\n" + str(e))
                tfLog.write("\n" + errorDelim)

        tfLog.write("\n"+buyDelim)
        tfLog.write("\nBuy Order Created:\n" + str(order))
        tfLog.write("\n"+buyDelim)
        print("Order Successfully created in order!")

        tfLog.close()

        #Create Sell Order
        return createSpotOcoSell(client, curSymbol,buyPrice, totalQuant, 4.9, 10, tfName)



    except Exception as e:
        tfLog = open(tfName, "a")
        tfLog.write("\n" + errorDelim)
        tfLog.write("\nError - " + str(e))
        tfLog.write("\n" + errorDelim)
        tfLog.close()
        print(e)


def createSpotOcoSell(client, curSymbol, curPrice, curQuant, takeProfitPerc, stopLossPerc, tfName):
    '''
    Assumes total currency value is always sold
    '''
    try:
        tfLog = open(tfName, "a")

        info = client.get_symbol_info(curSymbol)
        precisionPrice = 8
        precisionQuant = 8
        for x in info["filters"]:
            if(x["filterType"] == "PRICE_FILTER"):
                precisionPrice = x["tickSize"].find('1')-x["tickSize"].find(".")
                #print("Found PrecisionPrice Sell!!!,", precisionPrice)
            if(x["filterType"] == "LOT_SIZE"):
                precisionQuant = x["stepSize"].find('1')-x["stepSize"].find(".")
                #print("Found PrecisionQuant Sell!!!,", precisionQuant)

        sellPrice = round(curPrice*(1+(takeProfitPerc/100)), precisionPrice)
        sellPriceTrig = round(curPrice*(1-(stopLossPerc/100)), precisionPrice) #stopPrice
        sellPriceSL = round(curPrice*(1-(stopLossPerc+0.05)/100), precisionPrice) #stopLimitPrice
        #print("Sell total Quant:", curQuant)

        order = {}

        try:
            order = client.create_oco_order(
                symbol = curSymbol,
                side = "SELL",
                quantity = curQuant,
                price = sellPrice,
                stopPrice = sellPriceTrig,
                stopLimitPrice = sellPriceSL,
                stopLimitTimeInForce = "GTC")
            print("Sell Order Successfully Created")

        except Exception as e:
            print("EXCEPTION:\n", e)
            tfLog.write("\n" + errorDelim)
            tfLog.write("\nSPOT order Failed:\n" + str(e))
            tfLog.write("\n" + errorDelim)

        tfLog.write("\n"+sellDelim)
        tfLog.write("\nSell Order Created:\n" + str(order))
        tfLog.write("\n"+sellDelim)
        tfLog.close()
        #print("SimOrders are", simOrders)
        return order



    except Exception as e:
            # error handling goes here
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

    
