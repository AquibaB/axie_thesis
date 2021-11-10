import pandas as pd

from axs_token_issuance import axs_token_data
from ronin_gateway import axs_ronin_gateway

##### Load data from AXS token analytics - https://etherscan.io/token/0xbb0e17ef65f82ab018d8edd776e8dd940327b28b?a=0x73b1714fb3bfaefa12f3707befcba3205f9a1162#tokenAnalytics

# Transform data into a dataframe
axs_token_issuance = pd.DataFrame(axs_token_data)
# Rename columns
axs_token_issuance.columns = ['Year', 'Month', 'Day', 'X','X','X','X','X', 'AXS Locked Balance', 'X', 'X']
# Drop irrelevant columns
axs_token_issuance = axs_token_issuance.drop(columns='X')
# Fix Month data (incorrectly one month earlier)
axs_token_issuance['Month'] = axs_token_issuance.Month +1
# Create Date column
axs_token_issuance['Date'] = pd.to_datetime(axs_token_issuance[['Year', 'Month', 'Day']])
# Set Date as index
axs_token_issuance = axs_token_issuance.set_index('Date')
# Drop Year, Month, Day columns
axs_token_issuance = axs_token_issuance.drop(columns=['Year', 'Month', 'Day'])
# Calculate daily AXS issuance
axs_token_issuance['Daily AXS Issuance'] = axs_token_issuance['AXS Locked Balance'].diff() * -1
# Calculate Circulating Supply
axs_token_issuance['AXS Circ. Supply per Contract'] = int(270000000) - axs_token_issuance['AXS Locked Balance']
axs_token_issuance = axs_token_issuance.drop(columns='AXS Locked Balance')

##### Load data from Ronin Gateway token analytics - https://etherscan.io/token/token-analytics?m=normal&contractAddress=0xbb0e17ef65f82ab018d8edd776e8dd940327b28b&a=0x1a2a1c938ce3ec39b6d47113c7955baa9dd454f2&lg=en

# Transform data into a dataframe
axs_ronin_locked = pd.DataFrame(axs_ronin_gateway)
# Rename columns
axs_ronin_locked.columns = ['Year', 'Month', 'Day', 'X','X','X','X','X', 'AXS in Ronin', 'X', 'X']
# Drop irrelevant columns
axs_ronin_locked = axs_ronin_locked.drop(columns='X')
# Fix Month data (incorrectly one month earlier)
axs_ronin_locked['Month'] = axs_ronin_locked.Month +1
# Create Date column
axs_ronin_locked['Date'] = pd.to_datetime(axs_ronin_locked[['Year', 'Month', 'Day']])
# Set Date as index
axs_ronin_locked = axs_ronin_locked.set_index('Date')
# Drop Year, Month, Day columns
axs_ronin_locked = axs_ronin_locked.drop(columns=['Year', 'Month', 'Day'])
# Calculate daily AXS issuance
axs_ronin_locked['Daily Chg. in AXS'] = axs_ronin_locked['AXS in Ronin'].diff()
