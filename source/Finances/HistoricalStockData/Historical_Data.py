
import yfinance as yf
import matplotlib.pyplot as plt

#%matplotlib inline
# Get the data for the stock AAPL
#data = yf.download('AAPL','2016-01-01','2019-08-01')


#print(data.head())


# Plot the close price of the AAPL
#data['Adj Close'].plot()
#plt.show()


msft = yf.Ticker("MSFT")
print(msft)
print(type(msft))

print(msft.earnings)

print(msft.dividends)
