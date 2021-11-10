import json
from re import A
from ipywidgets.widgets import widget
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

from axs_token_issuance import axs_token_data
from ronin_gateway import axs_ronin_gateway
from data import revenue, treasury, slp_issuance, volume, issuance, axie_mc, growth
from etherscan_data import axs_token_issuance, axs_ronin_locked

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# Create a 2-Series function to plot the desired metrics

def make_plot(Series1, Series2):
    '''
    Plotly graphs composed of 2 Series with secondary y-axis

    Args:
        Series1: A Series of on-chain metric
        Series2: A Series of on-chain metric
    
    Returns:
        A plotly fig ready for customization
    '''
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Line(x=Series1.index, y=Series1, name=Series1.name),
        secondary_y=False,
    )

    fig.add_trace(
        go.Line(x=Series2.index, y=Series2, name=Series2.name),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        #title_text="BTC Issuance vs Market Cap",
        width=1000,
        height=500
    )
    
    return fig

###########
# SLP MK CAP PLOT 
###########

# Create a line graph of SLP's Market Capitalization and Price
slp_mk_fig = make_plot(axie_mc['SLP Mk Cap'], axie_mc['SLP Price'])

# single line px.line(axie_mc, x=axie_mc.index, y='SLP Mk Cap')

# Add figure title, legend, and size
slp_mk_fig.update_layout(
    title_text="SLP Market Cap and Price (USD)",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=0.2
))
# Set x-axis title
slp_mk_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
slp_mk_fig.update_yaxes(title_text="SLP Market Cap (USD, Log)", secondary_y=False, tickformat="$,.0f", type='log', showgrid=False, nticks=5)
slp_mk_fig.update_yaxes(title_text="SLP Price (USD, Log)", secondary_y=True, showgrid=False, nticks=5, type='log', tickformat=",.2f")

slp_mk_fig.update_traces(fill='tozeroy', secondary_y=False, line_color='grey')

###########
# AXS MK CAP PLOT
###########

# Create a line graph of AXS's Market Capitalization and Price
axs_mk_fig = make_plot(axie_mc['AXS Mk Cap'], axie_mc['AXS Price'])

# single line px.line(axie_mc, x=axie_mc.index, y='SLP Mk Cap')

# Add figure title, legend, and size
axs_mk_fig.update_layout(
    title_text="AXS Market Cap and Price (USD)",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=0.2
))
# Set x-axis title
axs_mk_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
axs_mk_fig.update_yaxes(title_text="AXS Market Cap (USD, Log)", secondary_y=False, tickformat="$,.0f", type='log', showgrid=False, nticks=5)
axs_mk_fig.update_yaxes(title_text="AXS Price (USD, Log)", secondary_y=True, showgrid=False, nticks=5, type='log', tickformat=",.2f")

axs_mk_fig.update_traces(fill='tozeroy', secondary_y=False, line_color='grey')

###########
# DAUs
###########
# Create a line graph of AXS's Market Capitalization and DAUs

dau_fig = make_plot(axie_mc['AXS Mk Cap'], growth['DAU (in-game battlers)'])

# single line px.line(axie_mc, x=axie_mc.index, y='SLP Mk Cap')

# Add figure title, legend, and size
dau_fig.update_layout(
    title_text="AXS Daily Active Users",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=0.3
))
# Set x-axis title
dau_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
dau_fig.update_yaxes(title_text="Market Cap (USD, Log)", secondary_y=False, tickformat="$,.0f", type='log', showgrid=False, nticks=5)
dau_fig.update_yaxes(title_text="DAUs (Weekly, Avg., Log)", secondary_y=True, showgrid=False, nticks=5, type='log', tickformat=",.0f")

dau_fig.update_traces(fill='tozeroy', secondary_y=False, line_color='grey')

###########
# Revenue
###########

# Create cumulative revenue from Ronin chain in USD
revenue_usd = revenue.copy()
revenue_usd = revenue_usd.loc[:,~revenue_usd.columns.str.contains('ETH')]
revenue_usd = revenue_usd.drop(columns='Date Raw')
revenue_usd['Total Fees USD'] = revenue_usd.sum(axis=1)
#revenue_usd.loc[revenue_usd['Land Presale USD']>0]
revenue_usd = revenue_usd.loc['2020-11-05':,:]
revenue_usd['Daily Revenue USD'] = revenue_usd['Total Fees USD'].diff()

# Create a line graph of AXS's Market Capitalization and Total Revenues/Fees

rev_fig = make_plot(axie_mc['AXS Mk Cap'], revenue_usd['Total Fees USD'])

# single line px.line(axie_mc, x=axie_mc.index, y='SLP Mk Cap')

# Add figure title, legend, and size
rev_fig.update_layout(
    title_text="AXS Total Revenues",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="left",
    x=-0.13
))
# Set x-axis title
rev_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
rev_fig.update_yaxes(title_text="Market Cap (USD, Log)", secondary_y=False, tickformat="$,.0f", type='log', showgrid=False, nticks=5)
rev_fig.update_yaxes(title_text="Revenues (USD, Log)", secondary_y=True, showgrid=False, nticks=5, type='log', tickformat=",.0f")

rev_fig.add_trace(
        go.Line(x=revenue_usd.index, y=revenue_usd['Marketplace Fee USD'], name='Marketplace Fee USD'),
        secondary_y=True,
    )

rev_fig.add_trace(
        go.Line(x=revenue_usd.index, y=revenue_usd['Breeding Fee USD'], name='Breeding Fee USD'),
        secondary_y=True,
    )

rev_fig.update_traces(fill='tozeroy', secondary_y=False, line_color='grey')

###########
# Breeding Data
###########

breeding_fig = make_plot(growth['DAU (in-game battlers)'], revenue_usd['Breeding Fee USD'])

breeding_fig.update_layout(
    title_text="Breeding Fees and DAUs",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="left",
    x=-0.05
))
# Set x-axis title
breeding_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
breeding_fig.update_yaxes(title_text="DAUs", secondary_y=False, tickformat=".0f",  showgrid=False, nticks=5)
breeding_fig.update_yaxes(title_text="Breeding Fees (USD)", secondary_y=True, showgrid=False, nticks=5,  tickformat=",.0f")

# Create a dataframe with the original breeding cost
breed_count = list(range(1,8))
slp_cost = [150, 300, 450, 750, 1200, 1950, 3150]
axs_cost = [2] * 7
data = list(zip(breed_count, slp_cost, axs_cost))

breeding_fee_orig = pd.DataFrame(data, index=breed_count, columns=['Breed #', 'SLP', 'AXS'])
breeding_fee_orig.set_index('Breed #')

# Create a dataframe with the adjusted breeding cost (Sep 23, 2021 - https://www.notion.so/aquiba/Sfermion-Axie-Infinity-ae0ad0b5487f4af592196ab17ad631f3#7bd8d85cd887459da18a878ec0b503d3)
breed_count = list(range(1,8))
slp_cost_adj = [600, 900, 1500, 2400, 3900, 6300, 10200]
axs_cost_adj = [1] * 7
data = list(zip(breed_count, slp_cost_adj, axs_cost_adj))

breeding_fee_adj = pd.DataFrame(data, index=breed_count, columns=['Breed #', 'SLP Adj.', 'AXS Adj.'])
breeding_fee_adj.set_index('Breed #')

###########
# Marketplace Volume
###########

volume = volume.loc['2020-11-04':,:]

vol_fig = make_plot(axie_mc['AXS Mk Cap'], volume['Total Cummulative Volume USD'])

vol_fig.update_layout(
    title_text="Marketplace Volume and Fees",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="left",
    x=-0.05
))
# Set x-axis title
vol_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
vol_fig.update_yaxes(title_text="Market Cap (USD, Log)", secondary_y=False, tickformat="$,.0f", type='log', showgrid=False, nticks=5)
vol_fig.update_yaxes(title_text="Marketplace Volume (USD, Log)", secondary_y=True, showgrid=False, nticks=5, type='log', tickformat=",.0f")

vol_fig.update_traces(fill='tozeroy', secondary_y=False, line_color='grey')

###########
# Treasury
###########

# Calculate Axie Infinity's USD Treasury balance
treasury['AXS'] = treasury['Breeding AXS']
treasury['ETH'] = treasury['Marketplace ETH']
treasury['AXS in USD'] = treasury['AXS'] * axie_mc['AXS Price']
treasury['ETH in USD'] = treasury['ETH'] * axie_mc['ETH Price']
treasury['Treasury in USD'] = treasury['AXS in USD'] + treasury['ETH in USD']

# Create a line graph of AXS's Market Capitalization and Axie Infinity's Treasury balance
treasury_fig = make_plot(axie_mc['AXS Mk Cap'], treasury['Treasury in USD'])

# single line px.line(axie_mc, x=axie_mc.index, y='SLP Mk Cap')

# Add figure title, legend, and size
treasury_fig.update_layout(
    title_text="Axie Infinity's Treasury",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="right",
    x=0.2
))
# Set x-axis title
treasury_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
treasury_fig.update_yaxes(title_text="Market Cap (USD, Log)", secondary_y=False, tickformat="$,.0f", type='log', showgrid=False, nticks=5)
treasury_fig.update_yaxes(title_text="Treasury (USD, Log)", secondary_y=True, showgrid=False, nticks=7, type='log', tickformat=",.0f")

treasury_fig.update_traces(fill='tozeroy', secondary_y=False, line_color='grey')

##########
# Discord
###########

discord_fig = make_plot(growth['DAU (in-game battlers)'], growth['Discord Members'])

discord_fig.update_layout(
    title_text="Discord Users and DAUs",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="left",
    x=-0.05
))
# Set x-axis title
discord_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
discord_fig.update_yaxes(title_text="DAUs", secondary_y=False, tickformat=".0f",  showgrid=False, nticks=5)
discord_fig.update_yaxes(title_text="Discord Users", secondary_y=True, showgrid=False, nticks=5,  tickformat=",.0f")

##########
# Issuance and AXS locked in Ronin
###########

# Create a copy of market data
axie_mc_supply = axie_mc.copy()
axie_mc_supply = axie_mc_supply.loc['2021-04-28':'2021-11-03',:]
axie_mc_supply.tail()

issuance_fig = go.Figure()

issuance_fig.add_trace(
    go.Line(x=axie_mc_supply.index, y=axie_mc_supply.loc[:'2021-11-02','AXS Circ. Supply per CoinGecko'], name='AXS Circ. Supply per CoinGecko')
    )
issuance_fig.add_trace(
    go.Line(x=axs_token_issuance.index, y=axs_token_issuance.loc[:'2021-11-02','AXS Circ. Supply per Contract'], name='AXS Circ. Supply per Contract')
    )
issuance_fig.add_trace(
    go.Line(x=axs_ronin_locked.index, y=axs_ronin_locked.loc[:'2021-11-02','AXS in Ronin'], name='AXS in Ronin')
    )

issuance_fig.update_layout(
    title_text="Issuance and Ronin sidechain",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="left",
    x=-0.05
))

issuance_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
issuance_fig.update_yaxes(title_text="AXS tokens", tickformat=".0f",  showgrid=False, nticks=10)


##########
# Market Cap of top Crypto games
###########

games_mc_fig = go.Figure()


# Axie Infinity
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['AXS Mk Cap'], name='Axie Infinity', legendrank=1)
)
# Decentraland
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['MANA Mk Cap'], name='Decentraland', legendrank=2)
)

# Splinterlans
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['SPS Mk Cap'], name='Splinterlands')
)

# Alien Worlds
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['TLM Mk Cap'], name='Alien Worlds')
)


# Star Atlas
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['ATLAS Mk Cap'], name='Star Atlas')
)

# The Sandbox
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['SAND Mk Cap'], name='The Sandbox')
)

# Illuvium
games_mc_fig.add_trace(
    go.Line(x=axie_mc.index, y=axie_mc['ILV Mk Cap'], name='Illuvium')
)


games_mc_fig.update_layout(
    title_text="Market Capitalization of top blockchain games",
    width=650,
    height=500,
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.5,
    xanchor="center",
    x=0.5
))

games_mc_fig.update_xaxes(title_text="Date", showgrid=False, nticks=20)
games_mc_fig.update_yaxes(title_text="Market Cap (USD, Log)", tickformat="$,.0f", type='log', showgrid=False, nticks=5)