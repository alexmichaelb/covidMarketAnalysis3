import apiFunctions

SP500IndexSymbol = ['FXAIX','SWPPX','VFINX','SVSPX','SPY']

SP500IndexPrice ={}

for fundSymbol in SP500IndexSymbol:
    fundPrice = apiFunctions.getPriceOfStock(fundSymbol)
    SP500IndexPrice[fundSymbol] = fundPrice

print(SP500IndexPrice)