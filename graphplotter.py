import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
#import pandas as pd

#Set colour styling for graphs, feel free to change
#list of styles: https://matplotlib.org/3.2.2/gallery/style_sheets/style_sheets_reference.html
style.use('default')

#Plot line graphs using this function. Useful for stock prices.
#Params: title of the graph, dataframe
def plotLineGraph(title, df,numOfDays):
    try:
        #Plot a line graph with stock figures
        plt.plot(df)
        #Display a legend to help navigate the graph
        plt.legend(df.columns)
        #Display a title
        plt.title(title)
        #Output graph
        plt.show()
    except:
        print("There was an error. Please check your dataframe.")

#Plots a histogram
#Params: title of the chart, dataframe, size of the chart.
def plotHist(title, df, chartSize):
    try:
        #Plot histogram
        df.hist(bins=50,figsize=((chartSize*2.5),chartSize*2))
        #Display histogram
        plt.show()
    except:
        print("There was an error. Please check your dataframe.")


#Plots a correlation graph
def plotCorrelation(title, df, chartSize):
    try:
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(chartSize,chartSize))
        ax.matshow(corr)
        #Display title
        plt.title=title
        #Display x axis with names
        plt.xticks(range(len(corr.columns)), corr.columns)
        #Display y axis with names
        plt.yticks(range(len(corr.columns)), corr.columns)
        #Display correlation graph
        plt.show()
    except:
        print("There was an error. Please check your dataframe.")

#Plots a standard graph
def plotGraph(title, df):
    #Plot graph
    plt.plot()
    plt.show()

#Plots a pie chart.
#Params: title of the chart, labels for the slices, the percentage of the pie, the distance to split the pie slice from the rest of the pie chart
def plotPieChart(title, labels, pieSizes, explode):
    #Define pie settings
    plt.pie(pieSizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True,startangle=90)
    #Making sure the pie is a circle
    plt.axis("equal")
    #Display title, ensuring that it doesn't block the pie chart
    plt.title(title, horizontalalignment='center', verticalalignment='top',y=1.08, bbox={'pad':5})
    #Display chart
    plt.show()

#Converts any string values that could be changed to boolean values, e.g: Yes = "1", No = "0"
def convertStringToBool(column, trueVal, falseVal):
    column = column.map({trueVal:1,falseVal:0})

#Will return the number of rows that matches the param for a column
#Params: dataframe, column to check, param to compare to
def getFilteredColumn(df, column, param):
    return len(df.loc[df[column] == param])