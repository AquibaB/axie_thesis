import json
from re import A
from ipywidgets.widgets import widget
import requests
import pandas as pd
import numpy as np
from pathlib import Path
#from pycoingecko import CoinGeckoAPI
from pathlib import Path
import time
import datetime
from datetime import datetime, timedelta, date
import csv
#from etherscan import Etherscan
import os
from dotenv import load_dotenv
load_dotenv()

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import hvplot.pandas

import streamlit as st

from axs_token_issuance import axs_token_data
from ronin_gateway import axs_ronin_gateway

from data import revenue, treasury, slp_issuance, volume, issuance, axie_mc, growth
from etherscan_data import axs_token_issuance, axs_ronin_locked
from plots import make_plot, slp_mk_fig, axs_mk_fig, dau_fig, rev_fig, breeding_fee_orig, breeding_fee_adj, breeding_fig, vol_fig, treasury_fig, discord_fig, issuance_fig, games_mc_fig


#########################################################################
# CREATE STREAMLIT APP
#########################################################################

sferion_logo_url = 'https://www.criptotendencias.com/wp-content/uploads/2021/11/Sfermion-cierra-una-ronda-de-financiacion-de-100-millones-de-dolares-para-la-industria-del-Metaverso.jpg'
axie_infiniti_logo_url = 'https://i.blogs.es/067b7e/axie-infinity-portada/1366_2000.jpg'

col1, col2 = st.columns(2)

with col1:
    st.image(sferion_logo_url, width=350)

with col2:
    st.image(axie_infiniti_logo_url, width=380)

st.markdown("## Axie Infinity Investment Thesis for Sfermion")
st.markdown("##### *By Aquiba Benarroch, CFA*")

####### RECOMMENDATION #######

st.markdown("---")
st.title("Recommendation")
st.markdown("---")

st.markdown("#### 1. Purchase and stake $AXS")
st.write("- Strong user monetization results in a sizable treasury accruing to AXS tokenholders.")
st.write("- Play-to-earn tokenomics and new gameplays attract players to Axie's ecosystem.")
st.write("- Sky Mavis' ownership of AXS (21% of total supply) aligns incentives with AXS holders.")
st.write("- The majority of AXS tokens are locked in the Ronin sidechain, indicating the ecosystem's strong participation by tokenholders in the ecosystem.")
st.write("- Staking AXS returns an attractive yield (~120% APR.)")

st.markdown("##### ")
st.markdown("#### 2. Consider purchasing Land NFTs, or wait for Land Phase II sale.")
st.write("- Land is the most valuable in-game scarce NFT. Only 25% of Lunacia's landmass has been sold.")
st.write("- Planned added functionality, such as custom Land gameplays and a Lunacia SDK to create virtual worlds, should add value to land NFTs.")

####### THESIS #######

st.markdown("---")
st.title("Thesis")
st.markdown("---")

st.write("Axie Infinity is the leading blockchain game in Web3. It has a high probability of being part of a future Metaverse because of 1) a growing network community (+2M current DAUs) and 2) vibrant token economics underpinned by NFTs generating income for players and fees for Axie Infinity.")
st.write("Sky Mavis is executing well on the Axie Infinity roadmap. The recent release of Ronin's Katana DEX (over $1B TVL) suggests that the team wants to position Ronin as the leading blockchain layer for crypto gaming, not just for Axie Infinity.")
st.write("AXS's market cap increased from $500M to $10B in the last ten months, driven by exponential user growth. New players fueled demand for Axies that led to an Axie breeding egg boom. As a result, Axie Infinity's revenues surpassed $1B over this timeframe (mostly from breeding fees.) AXS' treasury, from which tokenholders will benefit in distributions, recently reached $3B.")
st.write("The game offers three kinds of NFTs: Axie, Land, and Item. The land is more desirable because supply is limited and is a central piece of future gameplay.")
st.write("Axie Infinity's bear case is that value creation depends on adding new players constrained by high entry costs (~$900 for 3 Axies.) However, Axie's P2E model mainly attracts players from EM, where Axie's income is higher than domestic salaries. In addition, sponsoring programs overcome the requirement for an initial capital outlay to onboard new players.")

####### TOKEN ECONOMICS #######

st.markdown("---")
st.title("Token economics")
st.markdown("---")

with st.expander("Key Metrics"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Revenues (LTM)", value="+$1 Billion")
    with col2:    
        st.metric(label="DAU (weekly avg.)", value="+2 Million")
    with col3:
        st.metric(label="Treasury Balance", value="+$3 Billion")
        
st.write("- Two types of in-game tokens:")
st.write("1. AXS is used for governance, collect breeding fees, and for earning staking rewards.")
st.write("2. SLP is minted in battles and burnt when breeding Axies.")

with st.expander("Market data"):
    st.markdown("2. $AXS is used for governance rights, breeding fee paid to Treasury, and for earning staking rewards.")
    st.write(axs_mk_fig, width=300)

    st.write(slp_mk_fig, width=300)
    # CHANGE IN SLP BREEDING FEES IN SEPT 28 AS THE PRICE OF SLP CRATERED BUT MK CAP STAYED - MINTING TOO MUCH SLP
    
st.write("- Revenues are generated from breeding fees (1 AXS/breed) and a 4.25% Marketplace fee.")
st.write("- The marketplace enables trading of NFT assets (Axies, Land, and Items) and onboarding new players. Cumulative volume from trading NFTs surpassed $3B.")
with st.expander("Fundamental data"):
    st.markdown("- Explosion in user growth was driven by the migration from Ethereum Mainnet to Ronin sidechain (April 28, 2021).")
    st.write(dau_fig, width=300)

    st.markdown("- New players create demand for new Axies that generage significant revenues for Axie Infinity.")
    #Over the last six months, Axie Infinity is the Dapp that has generated the most revenue, ahead of Uniswap or OpenSea, only behind ETH")
    st.write(rev_fig, width=300)

    st.markdown("- Breeding fees have continued to increase despite Axie's cut in breeding take-rate from 2 AXS to 1 AXS on September 23, 2021")
    st.write(breeding_fig, width=350)

    st.markdown("- Axie's NFT Markeplace has seen cumulative volume of ~$3B and generated a 4.25% fee on every transaction.")
    st.write(vol_fig, width=300)

    st.markdown("- Axie Infinity's treasury grew from $5K to over $3 Billion that accrues to AXS holders.")
    st.write(treasury_fig, width=300)

st.write("- P2E model allows players from EM (mainly from the Philippines and Indonesia, countries with large populations and young demographics) to earn higher incomes than domestic salaries.")
with st.expander("Country demographics"):
    col1, col2 = st.columns(2)
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Philippines_single_age_population_pyramid_2020.png/1024px-Philippines_single_age_population_pyramid_2020.png', width=300)
    with col2:
        st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Indonesia_single_age_population_pyramid_2020.png/350px-Indonesia_single_age_population_pyramid_2020.png', width=300)

####### TEAM #######

st.markdown("---")
st.title("Sky Mavis Team")
st.markdown("---")

st.write("- Sky Mavis' ownership of AXS (21% of total supply) aligns incentives with AXS holders.")
with st.expander("AXS Allocations and Unlock schedule"):
    st.image('https://whitepaper.axieinfinity.com/~/files/v0/b/gitbook-28427.appspot.com/o/assets%2F-LocuLeNcXinpTOZxNu0%2F-MK0X0TNxIlYefrYZalV%2F-MK0XP8l-pUvJGy-DQLd%2FAxie%20Infinity%20Shards%20complete%20release%20schedule.png?alt=media&token=8e28c856-7dcd-44e0-9fd3-30aacca283ac')

st.write("- The Sky Mavis team, led by CEO Trung Nguyen and COO Aleksander Larsen, has broad crypto expertise.")
st.write("- In addition to the core game, Sky Mavis is building the Ronin ecosystem: Ethereum sidechain, wallet, staking AXS, and DEX Katana to swap tokens and farm WRON. The team is also considering a rollup to replace the sidechain and inherit Ethereum's security.")
with st.expander("Roadmap (May 2021)"):
    st.image('./data/roadmap.png')

####### COMMUNITY #######

st.markdown("---")
st.title("Community")
st.markdown("---")

st.write("- A vibrant community creates loyalty to Axie Infinity and discourages churn.")
st.write("- Axie Infinity's Discord channel is usually complete (capped at 800K members.)")
st.write("- Users continually create content to help players, like Axie World (guides, tools, and economics), Chillaxie (marketplace insights and breeding tool), or Axie Pulse (newsletter).")
with st.expander("Discord data"):
    st.write(discord_fig, width=300)    

st.write("- The majority of AXS tokens (~70%) are locked in the Ronin sidechain, indicating strong participation by tokenholders in the ecosystem.")

####### MARKET #######

st.markdown("---")
st.title("Crypto gaming market")
st.markdown("---")

st.write("- The industry has seen tremendous growth in recent months. Some tokens have reached record valuations even before games are launched, and most use the P2E model pioneered by Axie Infinity.")
with st.expander("Market capitalization of top crypto games"):
    st.write(games_mc_fig, width=300)

st.write("- Even though many games use BSC for hosting, new L2 solutions such as Immutable X aim to become the standard NFT gaming solution on Ethereum.")

####### RISKS #######

st.markdown("---")
st.title("Risks")
st.markdown("---")

st.write("- A slowdown in new player sign-ups is likely to hurt the Axie Infinity ecosystem. Possible catalysts include SLP price declines, delays in implementing new features, or competition.")
with st.expander("Change in Axie economics (Sep 23, 2021)"):
    st.write("- SLP price decline was driven by excessive minting of SLP which prompted an adjustment in breeding costs.")
    st.write(slp_mk_fig)
    #st.markdown("# ")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original breeding cost")
        st.write(breeding_fee_orig, width=300)
    with col2:
        st.write("Adjusted breeding costs")
        st.write(breeding_fee_adj, width=300)
    
    
st.write("- A downturn in the market for NFTs would diminish the value of the NFT assets in Axie Infinity.")
st.write("- Resumed issuance of AXS, after months on pause due to Ronin migration, is a tailwind to prices, although likely net positive for staking AXS.")
with st.expander("On-chain analysis"):
    st.write(issuance_fig, width=300)

