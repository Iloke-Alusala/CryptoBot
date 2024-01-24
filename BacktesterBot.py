# Get data of all prices from cryptobot


# Load the necessary packages and modules
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from DataCollectCandleStick import *
from datetime import datetime, timedelta
import json
from myCryptSim import *

def save_dataframes_to_csv(filename, dataframes):
    try:
        # Combine DataFrames into one DataFrame
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        # Save the combined DataFrame to a CSV file
        combined_df.to_csv(filename, index=False)
        print(f'DataFrames saved to {filename}')
    except Exception as e:
        print(f'Error while saving data to {filename}: {e}')


def split_dataframe_by_delimiter(df, delimiter_column='curPair'):
    '''
    returns an array of dataframes
    '''
    # Find rows where the delimiter column is populated
    delimiter_rows = df[df[delimiter_column].notnull()].index.tolist()

    # Initialize an array to store separate DataFrames
    separate_dataframes = []

    # Split the DataFrame into separate DataFrames using the delimiter rows
    for i in range(len(delimiter_rows)):
        start_row = delimiter_rows[i]
        end_row = delimiter_rows[i+1] if i+1 < len(delimiter_rows) else None

        # Create a separate DataFrame by selecting the rows between delimiter rows
        separate_df = df.iloc[start_row:end_row]

        # Reset the index to start from 0
        separate_df.reset_index(drop=True, inplace=True)

        # Append the separate DataFrame to the array
        separate_dataframes.append(separate_df)
    print("Split Complete ✅")
    
    return separate_dataframes

def convert_map_to_array(map_data):
    """
    Converts a map in the format {String: dataframe} to an array of dataframes.

    Parameters:
    - map_data: Dictionary with format {String: dataframe}.

    Returns:
    - Array of dataframes with the first row containing the key as 'CurPair'.
    """

    array_of_dataframes = []

    # Iterate through each key-value pair in the map
    for key, df in map_data.items():
        # Insert a row into the first position with 'CurPair' as key
        first_row = pd.DataFrame({"curPair": [key]})
        
        # Concatenate the first row with the original dataframe
        df_with_key = pd.concat([first_row, df], ignore_index=True)
        df_with_key.reset_index(drop=True, inplace=True)
        
        # Append the new dataframe to the array
        array_of_dataframes.append(df_with_key)

    return array_of_dataframes

def dataframe_to_map(df):

    result = {}
    for x in df:
        # Check if the DataFrame is empty
        if x.empty:
            return None
        # Extract the 'curPair' value from the first row
        curPair = x.loc[0, 'curPair']

        # Remove the first row
        dfNew = x.iloc[1:]
        
        dfNew.reset_index(drop=True, inplace=True)
        # Convert the DataFrame to a dictionary with 'curpair' and 'df' components
        result[curPair] = dfNew
    print("Conversion from dataframe to map Successful ✅")
    return result

def formatCurInfo(tfName):
    result = {}
    with open(tfName, 'r') as file:
        tmp = json.load(file)
        
    for x in tmp:
        try:
            if(x != "None"):
                result[x["symbol"]] = x
        except:
            pass
    print("Formatting of currency info complete: ✅")
    return result
    

def extract_rows(dataframe, start_row, end_row):
    if (start_row > end_row):
        raise ValueError("Start row must be less than or equal to end row.")

    if (start_row < 0) or (end_row >= len(dataframe)):
        raise ValueError("Invalid row indices.")

    # Extract rows from start_row to end_row
    selected_rows = dataframe.iloc[start_row:end_row + 1]
    selected_rows.reset_index(drop=True, inplace=True)

    return selected_rows

def align_dataframes(df_dict, df_main):
    """
    Aligns dataframes in a dictionary with a main dataframe.

    Parameters:
    - df_dict: Dictionary with format {"CurrencyPair": dataframe}.
    - df_main: Main dataframe with the desired length.

    Returns:
    - Aligned dictionary with format {"CurrencyPair": aligned dataframe}.
    """

    aligned_dict = {}

    # Iterate through each key-value pair in the dictionary
    for currency_pair, df_arr in df_dict.items():
        # Check if the length of df_arr is less than that of df_main
        if len(df_arr) < len(df_main):
            # Calculate the number of rows needed to fill
            rows_to_fill = len(df_main) - len(df_arr)
            
            # Fill df_arr with rows by copying the first row
            fill_rows = pd.concat([df_arr.iloc[[0]]] * rows_to_fill, ignore_index=True)
            
            # Concatenate the filled rows with the original df_arr at the beginning
            aligned_df = pd.concat([fill_rows, df_arr], ignore_index=True)
            aligned_df.reset_index(drop=True, inplace=True)
            #print("Realigned:", currency_pair)
            #print(aligned_df)
            
            # Update the dictionary with the aligned dataframe
            aligned_dict[currency_pair] = aligned_df
        else:
            # If df_arr is already of the same length, use it as is
            aligned_dict[currency_pair] = df_arr

    print("REALIGNMENT SUCCESSFUL: ✅")
    return aligned_dict
    


def backtest_get_all_tickers(index, dfs):
    data = []
    if(index<=len(dfs[0])):
        for x in dfs:
            try:
                data.append({'symbol': x.iloc[0]['curPair'], 'price' : str(x.iloc[index]['Close'])})
            except Exception as e:
                print("Found error for:", x.iloc[0]['curPair'])
                print("looks like:", x)
            
    # returns format: [{'symbol' : 'AGLDUSDT', 'price' : '0.88'}, {'symbol' : 'MATICUSDT', 'price' : '0.6559'}]
    
    return data


def populateSim(start, end, timeInterval, fileName):
    '''
    start : the first day of data collection
    end : the final day of data collection. If current day or forward, will collect up to most recent prices
    timeInterval : the time interval of data collection : 1m ,5m, 1h, 6h ... etc.
    '''
    # Load currency names
    client = setupClient()
    currency_names = getCurrencyNames(client)

    #Extract and store data of all margin currencies

    data = []

    print("Starting Data Collection🛩️")
    for x in currency_names:

        try:
            price_df = get_Historical_KLine_Data_OHLC(x, timeInterval, start, end)
            cols = list(price_df.columns)
            cols.append("curPair")
            symbol_df = pd.DataFrame(columns=cols)
            symbol_df.loc[len(symbol_df)] = {'curPair':x}
            
            #df2 = df.append(pd.DataFrame([new_row],index=['Index'],columns=df.columns))
            #print(df2)

            curBuffer = [''] * (len(price_df))
            price_df['curPair']=curBuffer

            # adds all the currencies to database
            data.append(symbol_df)
            data.append(price_df)
        except Exception as e:
            print("Failed to collect data for:", x)
            print("Sorry I failed you master. I hope it doesn't have too much of a lasting effect")
            print("Error:", e)
        
    # saves the database to a .csv file
    save_dataframes_to_csv(fileName, data)
    #print(data)
    print("Collection Complete")

#populateSim('2023-11-29', '2023-12-01', '1m', "1stLog.csv")

#df = pd.read_csv("1stLog.csv")
#separated = split_dataframe_by_delimiter(df, "curPair")
    

'''

# Example usage
if __name__ == "__main__":
    # Create DataFrames for currency symbols and prices
    currency_dataframes = []

    currencies = ['USD', 'EUR', 'GBP']
    for currency in currencies:
        symbol_df = pd.DataFrame({'Currency': [currency]})
        price_df = pd.DataFrame({'Currency': [None], 'Price': [1.15, 0.92, 1.3]})

        currency_dataframes.extend([symbol_df, price_df])

    # Save the combined DataFrames to a CSV file
    save_dataframes_to_csv('combined_currency_data.csv', currency_dataframes)

# Function to extract the data of the latest DataFrame record from the CSV file
def extract_latest_dataframe_data(filename):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename)
        
        if not df.empty:
            # Extract the last row (latest record)
            latest_record = df.iloc[-1]
            return latest_record
        else:
            print('CSV file is empty.')
    except Exception as e:
        print(f'Error while extracting data from {filename}: {e}')

# Function to retrieve prices of each currency from the CSV file
def retrieve_currency_prices(filename, currency_column):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filename)
        
        if not df.empty:
            # Group the data by the currency_column and return DataFrames for each currency
            currency_dfs = [group for _, group in df.groupby(currency_column)]
            return currency_dfs
        else:
            print('CSV file is empty.')
    except Exception as e:
        print(f'Error while retrieving currency prices from {filename}: {e}')
    
# Example usage
if __name__ == "__main__":
    # Create some sample DataFrames
    dataframes = [pd.DataFrame({'Currency': ['USD', 'USD', 'EUR', 'EUR'],
                                'Price': [1.1, 1.2, 0.9, 0.95]}),
                  pd.DataFrame({'Currency': ['USD', 'EUR', 'GBP'],
                                'Price': [1.15, 0.92, 1.3]})]

    # Save the DataFrames to a CSV file
    save_dataframes_to_csv('currency_prices.csv', dataframes)

    # Retrieve prices of each currency from the CSV file
    currency_dfs = retrieve_currency_prices('currency_prices.csv', 'Currency')
    
    if currency_dfs is not None:
        for i, df in enumerate(currency_dfs):
            currency = df['Currency'].iloc[0]  # Get the currency label
            print(f'Prices for {currency}:')
            print(df)
'''





    

