import urllib.request
import json

def getPriceOfStock(companySymbol, numOfDays):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+companySymbol+"&outputsize=full&apikey=Y11HUWNU7HM58RRL"
    json_obj = urllib.request.urlopen(url)

    data = json.load(json_obj)
    dates = data["Time Series (Daily)"]
    final_prices = []
    counter = 0
    for day in dates:
        counter += 1
        if counter > numOfDays:
            break
        prices = dates[day]
        priceNum = float(prices['4. close'])
        final_prices.append(priceNum)
    print(len(final_prices))
    print(companySymbol+" Done")
    return final_prices

def bundleStockPrices(arrayOfCompanySymbols, numOfDays):
    bundledStock = {}
    for fundSymbol in arrayOfCompanySymbols:
        fundPrice = getPriceOfStock(fundSymbol,numOfDays)
        bundledStock[fundSymbol] = fundPrice
    return bundledStock