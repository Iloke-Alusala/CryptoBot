# Package to calculate moving average

# Load the necessary packages and modules
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from DataCollectCandleStick import *
from datetime import datetime, timedelta
from BacktesterBot import *

# Simple Moving Average - over duration 1 minute, 1 hour, 4 hour
# Over a period of the last 2 days
# Returns 1, 0, -1 --> checks if gradient passes certain threshold
# Calculate the 1-minuteSMA

def LocateTriggers(trig, gSMA, roundVal, trigBuffer):
    '''
    trig: Trigger gradient value
    gSMA: Array containing gradients
    roundVal: decimals to round off gradient value to
    trigBuffer: Region around trigger that is still considered a valid trigger
    '''
    marked_x = []
    marked_y = []
    preval = -1
    
    for i in range(len(gSMA)):
        if(not pd.isna(gSMA[i])):
            if(preval != -1):
                val = float(gSMA[i])
                rval = round(val, roundVal)
                if(((rval < trig+trigBuffer) and(rval > trig-trigBuffer)) and (preval < rval)):
                    #print("preval:", preval,"rval:", rval)
                    marked_x.append(i)
                    marked_y.append(val)
            preval = float(gSMA[i])
            
    return marked_x, marked_y

def LocateTrioTriggers(trig1, trig2, trig3, gSMA1, gSMA2, gSMA3, roundVal, trigBuffer1, trigBuffer2, trigBuffer3):
    '''
    trig: Trigger gradient value
    gSMA: Array containing gradients
    roundVal: decimals to round off gradient value to
    trigBuffer: Region around trigger that is still considered a valid trigger
    '''
    marked_x = []
    marked_y = []
    preval1 = -1
    preval2 = -1
    preval3 = -1
    immediateTrigger = False

    try:
        for i in range(1, len(gSMA1)):
            if((not pd.isna(gSMA1[i])) and (not pd.isna(gSMA2[i])) and (not pd.isna(gSMA3[i]))):
                if((preval1 != -1) and (preval2 != -1) and (preval3 != -1)):

                    
                    val1 = float(gSMA1[i])
                    val2 = float(gSMA2[i])
                    val3 = float(gSMA3[i])
                    
                    rval1 = round(val1, roundVal)
                    rval2 = round(val2, roundVal)
                    rval3 = round(val3, roundVal)
                    
                    if((((rval1 > trig1-trigBuffer1)) and (preval1 < rval1)) and
                       (((rval2 > trig2-trigBuffer2)) and (preval2 < rval2)) and
                       (((rval3 > trig3-trigBuffer3)) and (preval3 < rval3))):
                        #print("preval:", preval,"rval:", rval)
                        marked_x.append(i)
                        marked_y.append(val1)
                        marked_x.append(i)
                        marked_y.append(val2)
                        marked_x.append(i)
                        marked_y.append(val3)
                        if(i==len(gSMA1)-1):
                            print("LENGTH MATCHED")
                            immediateTrigger = True
                preval1 = float(gSMA1[i])
                preval2 = float(gSMA2[i])
                preval3 = float(gSMA3[i])
        return marked_x, marked_y, immediateTrigger

    except Exception as e:
        print("Oops, something went wrong in LocateTrioTriggers")
        print(e)

def getSMAGradient(SMA, smoothWindow):
    '''
    return an array with smoothed respective gradient of SMA
    SMA : Array of SMA
    smoothWindow : Window over which to smooth gradient values
    '''
    try:
        newSMA = pd.Series(SMA)
        #print("err1")
        for i in range(1, len(newSMA)):
            #print("err2")
            if(not pd.isna(newSMA[i])):
                #print("err3")
                rec1 = newSMA[i]
                break

        if('e' in str(rec1).lower()):
            #print("err4")
            rec1 = "{:.6f}".format(float(rec1))
        # Normalise data values for accurate gradient calculations
        if(float(rec1) >= 1):
            #print("err5")
            newSMA = newSMA * 10**(-(len(str(int(rec1)))-1))
            
        elif(float(rec1) < 1):
            #print("SMA[0]:", float(rec1))
            mult = 0
            #print("In 2nd format place")
            #print("err6")
            for i in range(len(str(rec1))-2):
                if(str(rec1)[2+i] != '0'):
                    #print("err8")
                    mult = i+1
                    #print("Mult is:", mult)
                    break
            newSMA = newSMA * 10**(mult)
            #print("err9")
        # Calculate gradients of differrent SMAs
        gSMA = newSMA.diff()*100
        # Set smoothing window size of gradient curves
        gSMA = gSMA.rolling(window=smoothWindow).mean()
        return gSMA

    except Exception as e:
        print("Oops, something failed in getSMAGradient")
        print("SMA is:", SMA)
        print(e)
    

    
    

def validSMA(thresh1, thresh2, thresh3, threshBuffer1, threshBuffer2, threshBuffer3, dur1, dur2, dur3, curSymbol, start, end, delayCnt):
    '''
    thresh1-3: gradient thresholds for repective SMA
    threshBuffer1-3: Region around threshold that is still a valid trigger
    dur1-3: duration as factors of 1min intervals
    curSymbol: symbol of currency
    start = dateTime String: "%Y-%m-%d-%H-%M"
    end = dateTime object: "%Y-%m-%d-%H-%M"
    delayCnt = delayed counters to consider found trigger, only applies to thresh1, dur1
    '''
    data = get_Historical_KLine_Data_Compressed(curSymbol, "1m", start, end)
    data["Date"] = pd.to_datetime(data['Date'])

    # Get all price data
    print(data)
    
    # Get initial SMA1, typical windowSize is 1
    oSMA1 = pd.Series(data["Close"].rolling(dur1).mean(), name = "SMA_"+str(dur1)+"min")
    oSMA2 = pd.Series(data["Close"].rolling(dur2).mean(), name = "SMA_"+str(dur2)+"min")
    oSMA3 = pd.Series(data["Close"].rolling(dur3).mean(), name = "SMA_"+str(dur3)+"min")

    print("Dur1:", dur1)
    print("Dur2:", dur2)
    print("Dur3:", dur3)
    
    gSMA1 = getSMAGradient(oSMA1, 10)
    gSMA2 = getSMAGradient(oSMA2, 10)
    gSMA3 = getSMAGradient(oSMA3, 10)

    print("gSMA1:\n",gSMA1)
    print("gSMA2:\n",gSMA2)
    print("gSMA3:\n",gSMA3)


    #print("SMA3 last:", SMA3.iloc[-1], "Second last:", SMA3.iloc[-2])

    plotSMAResults('Close Price and SMAs of '+ curSymbol, 'Gradient of SMAs', data, oSMA1, oSMA2, oSMA3, 'SMA1','SMA2','SMA3', gSMA1, gSMA2, gSMA3, 'gSMA1','gSMA2','gSMA3', '%Y-%m-%d',
                   thresh1, thresh2, thresh3, threshBuffer1, threshBuffer2, threshBuffer3, 'x')

    if(valid1 and valid2 and valid3):
        return 1
    if(valid1 and valid2 and (not(valid3))):
        return 0
    if(valid1 and valid3 and(not(valid2))):
        return 0.5
    return -1

def valideSMA(thresh1, thresh2, thresh3, threshBuffer1, threshBuffer2, threshBuffer3, dur1, dur2, dur3, curSymbol, start, end):
    '''
    thresh1-3: gradient thresholds for repective SMA
    threshBuffer1-3: Region around threshold that is still a valid trigger
    dur1-3: duration as factors of 1min intervals
    curSymbol: symbol of currency
    start = dateTime String: "%Y-%m-%d"
    end = dateTime object: "%Y-%m-%d"
    '''
    print("testing:", curSymbol)
    #print("Data checker:")
    #print('index:', index)
    #print('df:', df)
    data = get_Historical_KLine_Data_Compressed(curSymbol, "1m", start, end)
    
    #data = extract_rows(df, max(0, index-dur3),index)
    #print("extracted data:", data)
    #data["Date"] = pd.to_datetime(data['Date'])

    # Get all price data
    #print("Past Data is:\n", data)

    # Set threshold buffer
    threshBuffer = 0.011
    try:
        # Get initial SMA1, typical windowSize is 1
        SMA1 = pd.Series(data["Close"].ewm(dur1).mean(), name = "eSMA_"+str(dur1)+"min")
        oSMA1 = pd.Series(data["Close"].ewm(dur1).mean(), name = "eSMA_"+str(dur1)+"min")
        oSMA2 = pd.Series(data["Close"].ewm(dur2).mean(), name = "eSMA_"+str(dur1)+"min")
        oSMA3 = pd.Series(data["Close"].ewm(dur3).mean(), name = "eSMA_"+str(dur1)+"min")

        # Generate SMA2, SMA3 from SMA1 since same as directly from data
        SMA2 = pd.Series(SMA1.ewm(dur2).mean(), name = "eSMA_"+str(dur2)+"min")
        SMA3 = pd.Series(SMA1.ewm(dur3).mean(), name = "eSMA_"+str(dur3)+"min")
        
        gSMA1 = getSMAGradient(SMA1, 10)
        gSMA2 = getSMAGradient(SMA2, 10)
        gSMA3 = getSMAGradient(SMA3, 10)

        #print("Successfully generated, gSMAs")
        #print("SMA3 last:", SMA3.iloc[-1], "Second last:", SMA3.iloc[-2])
        
        immediateTrigger = plotSMAResults('Close Price and eSMAs of '+ curSymbol, 'Gradient of eSMAs', data, oSMA1, oSMA2, oSMA3, 'eSMA1','eSMA2','eSMA3', gSMA1, gSMA2, gSMA3, 'geSMA1','geSMA2','geSMA3', '%Y-%m-%d',
                       thresh1, thresh2, thresh3, threshBuffer1, threshBuffer2, threshBuffer3, 'o')

        
        return immediateTrigger
    except Exception as e:
        print("Something failed in ValideSMA")
        print(e)
    '''
    if(valid1 and valid2 and valid3):
        return 1
    if(valid1 and valid2 and (not(valid3))):
        return 0
    if(valid1 and valid3 and(not(valid2))):
        return 0.5
    return -1
    '''

def plotSMAResults(L_ax1_title, L_ax2_title, data, oSMA1, oSMA2, oSMA3, L_oSMA1, L_oSMA2, L_oSMA3, gSMA1, gSMA2, gSMA3, L_gSMA1, L_gSMA2, L_gSMA3, dateFormat, thresh1, thresh2, thresh3,
                   threshBuffer1, threshBuffer2, threshBuffer3, markSymbol):
    try:
        
        #Set axles ready for plotting
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
        
        # Plot SMA and close price on graphs
        ax1.set_title(L_ax1_title)
        ax1.set_ylabel('Price')
        ax1.plot(data.index, data['Close'], 'y', lw=1, label='Close Price')
        ax1.plot(oSMA3.index, oSMA3, 'g', lw=1, label= L_oSMA3)
        ax1.plot(oSMA2.index, oSMA2, 'r', lw=1, label= L_oSMA2)
        ax1.plot(oSMA1.index, oSMA1, 'b', lw=1, label= L_oSMA1)
        ax1.legend()
        
        ax2.set_title(L_ax2_title)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Gradient')
        ax2.plot(gSMA3.index, gSMA3, 'g', lw=1, label= L_gSMA3)
        ax2.plot(gSMA2.index, gSMA2, 'y', lw=1, label= L_gSMA2)
        ax2.plot(gSMA1.index, gSMA1, 'b', lw=1, label= L_gSMA1)
        
        ax2.legend()
        
        ax1.xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter(dateFormat))

        plt.setp(ax1.get_xticklabels(), rotation=45)
        plt.setp(ax2.get_xticklabels(), rotation=45)
        
        
        # Calculate locations of price triggers
        marked_x1, marked_y1, immediateTrigger = LocateTrioTriggers(thresh1, thresh2, thresh3, gSMA1, gSMA2, gSMA3, 6, threshBuffer1, threshBuffer2, threshBuffer3)
        valid1 = False
        valid2 = False
        valid3 = False
        if(len(marked_x1)>0):
            valid1 = (marked_x1[-1]==len(gSMA1))

        
        print("Immediate Trigger:", immediateTrigger)
          
        plt.scatter(marked_x1, marked_y1, color='red', marker=markSymbol, s=20, label='X')
        plt.tight_layout()
        plt.show()
        
        return immediateTrigger
    
    except Exception as e:
        print("Oops, something failed in plotSMAResults")
        print(e)

def rsi(close, periods = 60):
    
    close_delta = close.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi
'''
data = get_Historical_KLine_Data_Compressed("SNTUSDT", "1m", "2023-10-30", "2023-11-02")
data["Date"] = pd.to_datetime(data['Date'])

# Call RSI function from the talib library to calculate RSI
data['RSI'] = rsi(data['Close'])

# Plotting the Price Series chart and the RSI below
fig = plt.figure(figsize=(10, 7))

# Define position of 1st subplot
ax = fig.add_subplot(2, 1, 1)

# Set the title and axis labels
plt.title('BTC Price Chart')
plt.xlabel('Date')
plt.ylabel('Close Price')

plt.plot(data['Close'], label='Close price')

# Add a legend to the axis
plt.legend()

# Define position of 2nd subplot
bx = fig.add_subplot(2, 1, 2)

# Set the title and axis labels
plt.title('Relative Strength Index')
plt.xlabel('Date')
plt.ylabel('RSI values')

plt.plot(data['RSI'], 'm', label='RSI')

# Add a legend to the axis
plt.legend()

plt.tight_layout()
plt.show()

'''
trig3 = 0.03
trigMult2 = 13
trigMult1 = 30
print("Final Result:------------", valideSMA(trig3*trigMult1 , trig3*trigMult2, trig3, 0.011, 0.011, 0.011, 1, 5, 240, "CKBUSDT", "2024-01-28", "2024-01-31"))



