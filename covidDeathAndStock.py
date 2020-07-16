#Used for pulling the data
import urllib.request 
import json
#Used for formatting the data
import pandas as pd
#Used for data visualisation
import matplotlib.pyplot as plt
from matplotlib import style

#Returns a pandaDF of the closing stock prices in the last x amount of days
def getPriceOfStock(companySymbol, numOfDays): 
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+companySymbol+"&outputsize=full&apikey=Y11HUWNU7HM58RRL"
    json_obj = urllib.request.urlopen(url)
    #Finds the data from the url
    data = json.load(json_obj)
    #Choosing the revelant key from the data dictionary
    dates = data["Time Series (Daily)"] 
    #Initializing lists to store the data
    final_prices = [] 
    calendar = []
    counter = 0
    #For-loop used to run through every trading day 
    for day in dates: 
        counter += 1
        #Limits the amount of data using the number of days wanted
        if counter > numOfDays: 
            break
        #Gets the stock's price - This will include Open, High, Low, Closed prices
        prices = dates[day]
        #Choosing the stock's closed price
        priceNum = float(prices['4. close']) 
        final_prices.append(priceNum)
        calendar.append(day)
    #Dictionary containing the company and it's stock prices 
    final_prices.reverse()
    calendar.reverse()
    stockDict = {companySymbol : final_prices} #CHANGE
    #Formatting the pulled data to a Panda DataFrame
    df = pd.DataFrame(data = stockDict, index = pd.to_datetime(calendar))
    return df
    
#NOTE: Alpha Vantage only allows 5 API calls a minute, 500 a day -> Can only have an input size of list size 5
#Function to format (multiple) stocks into a PandaDF and alligns the dates
def bundleStockPrices(arrayOfCompanySymbols, numOfDays):
    largeTable = getPriceOfStock(arrayOfCompanySymbols[0], numOfDays) 
    del arrayOfCompanySymbols[0]
    for symbol in arrayOfCompanySymbols:
        smallTable = getPriceOfStock(symbol, numOfDays)
        #Concatenating the tables together -> will provide the intersection of all the data -> will provide <= 200 day data values
        #largeTable = pd.concat([largeTable, smallTable.reindex(largeTable.index)], axis = 1)
        largeTable = pd.concat([largeTable, smallTable], axis = 1, join ='inner')
    print("Any null data: "+str(largeTable.isnull().values.any()))
    print(largeTable.head())
    print("...")
    print(largeTable.tail())
    return largeTable

SP500TickerSymbol = ['FXAIX','SWPPX','VFINX','SPY']
SP500_fund_prices = bundleStockPrices(SP500TickerSymbol, 200)

def plotLineGraph(title, df):
    try:
        #Opens the figure
        plt.figure()
        #Plot the stock data points
        df.plot()
        #Display a title
        plt.title(title)
        #Display a legend to help navigate the graph
        plt.legend(df.columns)
    except:
        print("There was an error. Please check your dataframe.")

plotLineGraph("Stock price of S&P index tracker funds", SP500_fund_prices)

airlineCompanies = ['DAL','AAL','DLAKF','UAL','AFRAF']
airline_prices = bundleStockPrices(airlineCompanies, 200)

plotLineGraph("Stock price of airline companies", airline_prices)
#To zoom in:
#plt.xlim(pd.to_datetime("2020-03-01"),pd.to_datetime("2020-04-01")) #Year-Month-Day

biomedicalCompanies = ['JNJ','RHHBF','SHTDF','PFE','GSK']
biomedical_prices = bundleStockPrices(biomedicalCompanies, 200)

plotLineGraph("Stock price of pharmaceutical companies", biomedical_prices)
#To zoom in:
#plt.xlim(pd.to_datetime("2020-03-01"),pd.to_datetime("2020-04-01")) #Year-Month-Day

def averagePctChange(table, industry):
    percentage_change = table.pct_change()
    percentage_change = percentage_change.drop(percentage_change.index[0])
    percentage_change[industry+" ROC"] = percentage_change.sum(axis = 1)
    percentage_change[industry+" ROC"] =  percentage_change[industry+" ROC"].map(lambda x: x/3)
    for column in table:
        if column == industry+" ROC":
            break
        del percentage_change[column]
    return percentage_change

SP500_APC = averagePctChange(SP500_fund_prices, "S&P500")
airline_APC = averagePctChange(airline_prices, "Aviation")
bio_APC = averagePctChange(biomedical_prices, "Pharmaceutical")
ROC_data  = pd.concat([SP500_APC, airline_APC, bio_APC], axis = 1, join ='inner')
plotLineGraph("Daily rate of change of price", ROC_data)
#To zoom in:
#plt.xlim(pd.to_datetime("2020-03-01"),pd.to_datetime("2020-04-01")) #Year-Month-Day

def plotCorrelation(title, df, chartSize):
    try:
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(chartSize,chartSize))
        ax.matshow(corr)
        #Display title
        plt.title = title
        #Display x axis with names
        plt.xticks(range(len(corr.columns)), corr.columns)
        #Display y axis with names
        plt.yticks(range(len(corr.columns)), corr.columns)
        #Display correlation graph
        plt.show()
    except:
        print("There was an error. Please check your dataframe.")

