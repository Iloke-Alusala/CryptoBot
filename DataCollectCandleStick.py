# Package to get CandleStick Data and Store historical Data

import time
from datetime import datetime, timezone
from binance.client import Client
from myCrypt import *

def get_Historical_KLine_Data (symbolPair, timeInterval, start, end):
    
    client  = setupClientCollector()
    # return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

    histData = client.get_historical_klines(symbolPair, timeInterval, start, end)
    keys = ["Date", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Number of Trades", "Taker buy base asset volume", "Taker buy quote asset volume"]
    histDataDict = []

    for x in histData:
        tmpx = list(x)
        tmpx[0] = datetime.fromtimestamp(x[0] / 1000.0, tz=timezone.utc).strftime('%Y-%m-%d')
        tmpx[6] = datetime.fromtimestamp(x[6] / 1000.0, tz=timezone.utc).strftime('%Y-%m-%d')
        tmpx[1] = float(x[1])
        tmpx[2] = float(x[2])
        tmpx[3] = float(x[3])
        histDataDict.append(dict(zip(keys, tmpx)))

    df = pd.DataFrame(histDataDict)
    #print(df["Open"])

    return df

def get_Historical_KLine_Data_Compressed (symbolPair, timeInterval, start, end):
    client  = setupClient()
    # return: list of OHLCV values (Open time, Open, High, Low, Close, Volume)

    histData = client.get_historical_klines(symbolPair, timeInterval, start, end)
    keys = ["Date", "Open", "High", "Low", "Close", "Volume", "Close Time"]
    histDataDict = []

    for x in histData:
        tmpx = []
        tmpx.append(datetime.fromtimestamp(x[0] / 1000.0, tz=timezone.utc).strftime('%Y-%m-%d'))
        tmpx.append(float(x[1]))
        tmpx.append(float(x[2]))
        tmpx.append(float(x[3]))
        tmpx.append(float(x[4]))
        tmpx.append(float(x[5]))
        histDataDict.append(dict(zip(keys, tmpx)))

    df = pd.DataFrame(histDataDict)
    #print(df["Open"])

    return df

def get_Historical_KLine_Data_OHLC(symbolPair, timeInterval, start, end):
    client  = setupClient()
    # return: list of OHLCV values (Open time, Open, High, Low, Close)

    histData = client.get_historical_klines(symbolPair, timeInterval, start, end)
    keys = ["Date", "Open", "High", "Low", "Close"]
    histDataDict = []

    for x in histData:
        tmpx = []
        tmpx.append(datetime.fromtimestamp(x[0] / 1000.0, tz=timezone.utc).strftime('%Y-%m-%d-%H-%M'))
        tmpx.append(float(x[1]))
        tmpx.append(float(x[2]))
        tmpx.append(float(x[3]))
        tmpx.append(float(x[4]))
        histDataDict.append(dict(zip(keys, tmpx)))

    df = pd.DataFrame(histDataDict)
    #print(df["Open"])

    return df
