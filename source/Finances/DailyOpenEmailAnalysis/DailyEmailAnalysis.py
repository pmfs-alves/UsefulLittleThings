# Necessary Libraries
import pandas as pd
import shutil, os, time, glob \
#for email
import  smtplib, ssl
#more specific ones for finance
import yfinance as yf
from get_all_tickers import get_tickers as gt   #pip install get-all-tickers
#docs for further development https://github.com/shilewenuw/get_all_tickers



# List of the stocks we are interested in analyzing.
#We create three lists:
# one for exploring other stocks
# one for a preselect favourites (you have domain knowledge, you know more about their behaviour or just plain like them
#and one so that your portfolio is also evaluated
#
new_tickers = gt.get_tickers_filtered(mktcap_min=150000, mktcap_max=10000000)
favourites = ["AMZN", "FB"]
current_portfolio =[]


# Check that the amount of tickers isn't more than 1800
print("The amount of stocks chosen to observe: " + str(len(tickers)))