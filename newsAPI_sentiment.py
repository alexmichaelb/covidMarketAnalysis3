import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import DateTime
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def getNews(qPhrase):
    # Retrieving news results and formatting into pandas df
    
    url = 'http://newsapi.org/v2/everything?'  # endpoint
    apiKey = '54f02afc70ed430381177f97c624d402'  # your own API key

    # Specify the query and number of returns
    parameters = {
        'q': qPhrase,  # query phrase
        'pageSize': 100,  # maximum is 100
        'apiKey': apiKey,
        'language': 'en',
        'from': '2020-24-03',  # earliest date
        'to': '2020-23-04',  # latest date (today) # THESE DATES AREN'T WORKING????
        'sort_by': 'popularity'
    }

    # Make the request
    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    
    df = pd.DataFrame(response_json['articles'])
    headers = ['title', 'content', 'source', 'publishedAt', 'url', 'Overall Sentiment', 'Positive Sentiment', 'Neutral Sentiment', 'Negative Sentiment']
    df = df.reindex(columns = headers)
    
    # Empty lists to add sentiment data to 
    overall_sent = []
    pos_sent = []
    neut_sent = []
    neg_sent = []
    
    # Find and add sentiment data
    for i in df.index:
        overall, positive, neutral, negative = getSentiment(df['title'][i])
        overall_sent.append(overall)
        pos_sent.append(positive)
        neut_sent.append(neutral)
        neg_sent.append(negative)

    df['Overall Sentiment'] = overall_sent
    df['Positive Sentiment'] = pos_sent
    df['Neutral Sentiment'] = neut_sent
    df['Negative Sentiment'] = neg_sent
        
    # Make publish column datetime object and sort into date order for easier analysis 
    df['publishedAt'] = df['publishedAt'].apply(lambda date: split_date_time_to_obj(date)) 
    df = df.sort_values(by='publishedAt')
    df = df.reset_index(drop=True)
    
    # Change overall sentiment to numerical values
    db_map = {"positive": 1, "neutral": 0, "negative": -1}
    df['Overall Sentiment'] = df['Overall Sentiment'].map(db_map)
        
    # Save to csv file
    newsToCsv(df, qPhrase)
    return df


def split_date_time_to_obj(date_time_string):
    # Split the date_time string since it is in the format yyyy-mm-ddTHH:MM:SS
    # Returns a datetime object

    datetime_str = ''.join(' '.join(date_time_string.split('T')).split('Z'))
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    return datetime_obj
    return df
    

def getSentiment(doc):
    # Sentiment analysis
    
    # Preventing errors when doc is empty 
    if doc is None: 
        return '', '', '', ''

    subKey = 'd164cafb1f5a40cebe3d8b5f9bd8b395'
    endpoint = 'https://jen.cognitiveservices.azure.com/'
    sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

    client = authenticate_client(subKey, endpoint) # setup a new client

    documents = [doc]
    response = client.analyze_sentiment(documents)[0]

    return response.sentiment, response.confidence_scores.positive, response.confidence_scores.neutral, response.confidence_scores.negative  

def newsToCsv(newsdf, subject, country = None):
    # Save data to a csv file.
    # NOTE: FILE PATH WILL NEED TO BE CHANGED DEPENDING ON JUPYTER OR VS/PYCHARM USE

    if country is None:
        country = 'gen' # general

    file_path_root = 'C:/temp/'
    file_name = "iBankSentimentAnalysis_" + country + "_" + subject + ".csv"
    
    # Save dataframe to csv file in jupyter project folder
    newsdf.to_csv(file_path_root + file_name, index = False)  


# NOTE: NOT SURE IF PLOTTING WILL WORK IN VS/PYCHARM SO FOR USE IN JUPYTER
def plotRes(df, subject = ''):
    # Plot overall sentiment against date
    
    fig, ax = plt.subplots()
    plt.scatter(df['publishedAt'].values, df['Overall Sentiment'].values, marker='o')
    
    # Set labels and limits
    ax.set_xlim([df['publishedAt'][0], df['publishedAt'][len(df_e) - 1]])
    ax.set_xlabel('Date')
    ax.set_ylabel('Overall Sentiment')
    ax.set_title('Overall Sentiment of ' + subject + ' news')
    
    # Format x axis dates
    weeks = mdates.WeekdayLocator(byweekday=1, interval=1, tz=None)
    weeks_fmt = mdates.DateFormatter('%Y-%m-%d')
    days = mdates.DayLocator(bymonthday=None, interval=1, tz=None)
    ax.xaxis.set_major_locator(weeks)
    ax.xaxis.set_major_formatter(weeks_fmt)
    ax.xaxis.set_minor_locator(days)
    
    plt.show()
    
    
def plotCompare(df1, df2):
    # Compare the overall sentiment of two dfs filled with news results 
    # e.g. df1 hsa covid results and df2 has market results 
    
    if df1['publishedAt'][0] < df2['publishedAt'][0]:
        start_date = df1['publishedAt'][0]
    else:
        start_date = df1['publishedAt'][0]
        
    if df1['publishedAt'][len(df1) - 1] < df2['publishedAt'][len(df2) - 1]:
        end_date = df1['publishedAt'][len(df2) - 1]
    else:
        end_date = df1['publishedAt'][len(df1) - 1]
        
    
    # Plot scatter graph
    fig, ax = plt.subplots()
    plt.scatter(df1['publishedAt'].values, df1['Overall Sentiment'].values, c = 'red', marker = 'x', label = 'Covid news')
    plt.scatter(df2['publishedAt'].values, df2['Overall Sentiment'].values, c = 'blue', marker='o', label = 'Stock news')
    
    # Set labels and limits
    ax.set_xlim([start_date, end_date])
    ax.set_xlabel('Date')
    ax.set_ylabel('Overall Sentiment')
    ax.set_title('Comparing the overall sentiment of Covid and Market news')
    plt.legend(bbox_to_anchor=(1.05, 1))
    
    # Format x axis dates
    weeks = mdates.WeekdayLocator(byweekday=1, interval=1, tz=None)
    weeks_fmt = mdates.DateFormatter('%Y-%m-%d')
    days = mdates.DayLocator(bymonthday=None, interval=1, tz=None)
    ax.xaxis.set_major_locator(weeks)
    ax.xaxis.set_major_formatter(weeks_fmt)
    ax.xaxis.set_minor_locator(days)
    
    plt.show()

    if __name__ == '__main__':
        getNews_new('coronavirus')