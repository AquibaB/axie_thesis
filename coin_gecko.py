import json
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from pycoingecko import CoinGeckoAPI
from pathlib import Path
import time
import datetime
from datetime import datetime, timedelta, date
import csv
from etherscan import Etherscan
import os
from dotenv import load_dotenv
load_dotenv()

# Script to parse the market capitalization of Axie Infinity
cg = CoinGeckoAPI()

pages = 2 # max 250 results per page

cg_id_list = ['axie-infinity', 'smooth-love-potion', 'ethereum', 'splinterlands', 'alien-worlds', 'decentraland', 'star-atlas', 'the-sandbox', 'illuvium']

# 1 year lookback period
period = 365 * 1 
price_dict = {}

# Create dataframe to hold the data
markets  = pd.DataFrame()

# Define dates for coingecko
time_end = datetime.now()
time_start = datetime.fromisoformat('2020-11-04')
delta = time_end - time_start
unixtime_start = int(time.mktime(time_start.timetuple()))
unixtime_end = int(time.mktime(time_end.timetuple()))

for token in cg_id_list:

    # Parse data for selected tokens from coingeck API
    token_data = cg.get_coin_market_chart_by_id(id=token, vs_currency='usd', days=delta.days,
                                                      from_timestamp=unixtime_start, to_timestamp=unixtime_end)
    # Timestamp of API call
    s_time = time.time()
    
    # Create dataframe with parsed data instance
    df = pd.DataFrame()
    df['date'] = [t[0] for t in token_data['prices']]
    df[f"{token} Price"] = [t[1] for t in token_data['prices']]
    df[f"{token} Mk Cap"] = [t[1] for t in token_data['market_caps']]
    
    # First data entry in the markets df
    if len(markets) == 0:
        markets['date'] = [t[0] for t in token_data['prices']]
        markets[f"{token} Price"] = [t[1] for t in token_data['prices']]
        markets[f"{token} Mk Cap"] = [t[1] for t in token_data['market_caps']]
        
    # Subsequent data entries from df are merged onto markets df
    else:
        markets = markets.merge(df, on='date', how='outer')
    
    # Limit of 50 calls per minute (60/50 = 1.2)
    # One call every 1.2 minutes
    e_time = time.time()
    while e_time - s_time <= 1.2:  
        e_time = time.time()
        pass

# Create Axie's dataframe and set the date as the index    
axie_mc = markets.copy()
axie_mc['date']=pd.to_datetime(axie_mc['date'], unit = 'ms')
axie_mc = axie_mc.set_index('date', drop=True)
# Calculate AXS in circulation

axie_mc = axie_mc.iloc[:delta.days-1,:]
axie_mc['AXS Circ. Supply per CoinGecko'] = axie_mc['axie-infinity Mk Cap'] / axie_mc['axie-infinity Price']
axie_mc.columns = ['AXS Price', 'AXS Mk Cap', 'SLP Price' ,'SLP Mk Cap', 'ETH Price', 'ETH Mk Cap', 'SPS Price', 'SPS Mk Cap', 'TLM Price', 'TLM Mk Cap', 'MANA Price', 'MANA Mk Cap', 'ATLAS Price', 'ATLAS Mk Cap', 'SAND Price', 'SAND Mk Cap', 'ILV Price', 'ILV Mk Cap', 'AXS Circ. Supply per CoinGecko']
#axie_mc = axie_mc.dropna()
axie_mc['ATLAS Mk Cap']=axie_mc['ATLAS Mk Cap'].replace(0, np.nan)
axie_mc['SPS Mk Cap']=axie_mc['SPS Mk Cap'].replace(0, np.nan)
axie_mc['TLM Mk Cap']=axie_mc['TLM Mk Cap'].replace(0, np.nan)
axie_mc['ILV Mk Cap']=axie_mc['ILV Mk Cap'].replace(0, np.nan)

# Save as CSV file
axie_mc.to_csv('./data/axie_mc.csv')