##function for pulling new covid cases from the API

def cumulativeCases(country):
    # setting variables for requests
    cumulativeCasesPerDay = []
    # country = "japan" ##doesn't work for united-states, united-kingdom,
    url = "https://api.covid19api.com/country/" + country + "/status/confirmed"

    fromdate = "2020-02-01T00:00:00Z"
    todate = "2020-07-13T00:00:00Z"
    payload = {}
    headers = {}
    params = {"from": fromdate, "to": todate}

    # response and json form of response
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    dataParse = response.json()

    cumaCasesList = []
    listLength = len(dataParse)
    for x in range(0, listLength):

        dailyCountryProfile = dataParse[x]
        todaysCases = dailyCountryProfile['Cases']
        cumaCasesList.append(todaysCases)


    return(cumaCasesList)