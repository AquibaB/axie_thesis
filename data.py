import pandas as pd
from pathlib import Path

# Read CSV files from Axie World
revenue = pd.read_csv(Path('./data/revenue.csv'), 
                      sep=';',
                      infer_datetime_format=True,
                      index_col="Date Parsed",
                      parse_dates=True
                     )

treasury = pd.read_csv(Path('./data/treasury.csv'), 
                      sep=';',
                      infer_datetime_format=True,
                      index_col="Date Parsed",
                      parse_dates=True
                     )

slp_issuance = pd.read_csv(Path('./data/slpIssuance.csv'), 
                      sep=';',
                      infer_datetime_format=True,
                      index_col="Date Parsed",
                      parse_dates=True
                     )

volume = pd.read_csv(Path('./data/totalVolume.csv'), 
                      sep=';',
                      infer_datetime_format=True,
                      index_col="Date Parsed",
                      parse_dates=True
                     )
issuance = pd.read_csv(Path('./data/issuance.csv'),
                       index_col='Date',
                       parse_dates=True,
                       infer_datetime_format=True,
                      )
issuance = issuance.iloc[:,2:10]
issuance = issuance.dropna()
issuance = issuance.replace(issuance.iloc[1,2], 0)
cols = issuance.columns
for col in cols:
    issuance[col] = issuance[col].str.replace(",", "").astype(float)
issuance = issuance.copy()

axie_mc = pd.read_csv(Path('./data/axie_mc.csv'),
                       index_col='date',
                       parse_dates=True,
                       infer_datetime_format=True,
                      )

growth = pd.read_csv(Path('./data/Axie Growth Data.csv'),
                       index_col='Date',
                       parse_dates=True,
                       infer_datetime_format=True,
                      )