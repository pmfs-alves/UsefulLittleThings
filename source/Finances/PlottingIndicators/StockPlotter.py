import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta    #calculations over time
import talib                                        #Calculating the technical analysis
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc #finance plotting
from matplotlib.pylab import date2num

#get current data and format as UTC timestamp for use on Yahoo Finance

today = datetime.today().strftime("%d/%m/%Y")
today = datetime.strptime(today + " +0000", "%d/%m/%Y %z")
to = int(today.timestamp())
print("to", to)
# Get date ten years ago as UTC timestamp
ten_yr_ago = today-relativedelta(months=1)
fro = int(ten_yr_ago.timestamp())
print("fro",fro)
interval="5m"

def get_price_hist(ticker):
    """
    Gets data from yahoo as csv and puts into dataframe
    :param ticker: str
    :return: data : pandas df
    """
    # Put stock price data in dataframe
    url = "https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={fro}&period2={to}&interval={interval}&events=history".format(ticker=ticker, fro=fro, to=to, interval=interval)
    print(url)

    data = pd.read_csv(url)

    # Convert date to timestamp and make index
    data.index = data["Date"].apply(lambda x: pd.Timestamp(x))
    data.drop("Date", axis=1, inplace=True)

    return data

#Let's calculate some indicators using talib (info on selected indicators on link

def get_indicators(data):
    # Get MACD  https://www.investopedia.com/terms/m/macd.asp
    data_for_talib = np.asarray( data['Close'])
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data_for_talib)

    # Get MA10 and MA30 https://www.investopedia.com/terms/m/movingaverage.asp
    data["ma10"] = talib.MA(data_for_talib, timeperiod=10)
    data["ma30"] = talib.MA(data_for_talib, timeperiod=30)

    # Get RSI https://www.investopedia.com/terms/r/rsi.asp
    data["rsi"] = talib.RSI(data_for_talib)
    return data

#Plotting charts
def plot_chart(data, n, ticker):

    # Filter number of observations to plot
    data = data.iloc[-n:]

    # Create figure and set axes for subplots
    fig = plt.figure()
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
    ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
    ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
    ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)

    # Format x-axis ticks as dates
    ax_candle.xaxis_date()

    # Get nested list of date, open, high, low and close prices
    ohlc = []
    for date, row in data.iterrows():
        openp, highp, lowp, closep = row[:4]
        ohlc.append([date2num(date), openp, highp, lowp, closep])

    # Plot candlestick chart
    ax_candle.plot(data.index, data["ma10"], label="MA10")
    ax_candle.plot(data.index, data["ma30"], label="MA30")
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=0.8)
    ax_candle.legend()

    # Plot MACD
    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.legend()

    # Plot RSI
    # Above 70% = overbought, below 30% = oversold
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
    ax_rsi.plot(data.index, data["rsi"], label="rsi")
    ax_rsi.legend()

    # Show volume in millions
    ax_vol.bar(data.index, data["Volume"] / 1000000)
    ax_vol.set_ylabel("(Million)")

    # Save the chart as PNG
    fig.savefig( ticker + ".png", bbox_inches="tight")

    plt.show()


nflx_df = get_price_hist("NFLX")
nflx_df

nflx_df2 = get_indicators(nflx_df)
nflx_df2

plot_chart(nflx_df2, 180, "NFLX")

