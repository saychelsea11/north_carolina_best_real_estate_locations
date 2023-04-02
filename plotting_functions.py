import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_neighborhoods_and_coordinates(df):
    plt.figure(figsize=(30,12))
    plt.scatter(df['longitude'],df['latitude'],alpha=0.5)
    for i in df.index:
      plt.annotate(df['neighborhood'].iloc[i],xy=(df['longitude'].iloc[i],df['latitude'].iloc[i]),xytext=(df['longitude'].iloc[i],df['latitude'].iloc[i]))
    plt.xlabel('Longitude',size=15)
    plt.ylabel('Latitude',size=15)
    plt.title('Mapping of neighborhood names and coordinates',size=20)
    plt.show()

def uni_scatterplot(df,y_metric,ylabel):
    #Function used to create a univariate (1 variable) plot for a provided variable in the dataset
    #Inputs: dataframe, column name in dataframe, y-axis label
    plt.figure(figsize=(36,10))

    plt.subplot(1,2,1)
    sns.scatterplot(data=df,x=df.index,y=y_metric,hue='County',s=100)
    for i in range(len(df['ZipCode'])):
        plt.annotate(str(df['ZipCode'].iloc[i]),xy=(df.index[i]+0.15,df[y_metric].iloc[i]+0.15),xytext=(df.index[i]+0.15,df[y_metric].iloc[i]+0.15),size=12)
    plt.xlabel('Index',size=15)
    plt.ylabel(ylabel,size=15)

    plt.subplot(1,2,2)
    sns.scatterplot(data=df,x=df.index,y=y_metric,hue='City',s=100)
    for i in range(len(df['ZipCode'])):
        plt.annotate(str(df['ZipCode'].iloc[i]),xy=(df.index[i]+0.15,df[y_metric].iloc[i]+0.15),xytext=(df.index[i]+0.15,df[y_metric].iloc[i]+0.15),size=12)
    plt.xlabel('Index',size=15)
    plt.ylabel(ylabel,size=15)

    plt.show()

def bi_scatterplot(df,x_metric,y_metric,xlabel,ylabel):
    #Function used to create a bivariate plot for 2 variables in the dataset
    #Inputs: dataframe, x-axis column name, y-axis column name, x-axis label, y-axis label
    plt.figure(figsize=(36,10))

    plt.subplot(1,2,1)
    sns.scatterplot(data=df,x=x_metric,y=y_metric,hue='County')
    for i in range(len(df['ZipCode'])):
        plt.annotate(str(df['ZipCode'].iloc[i]),xy=(df[x_metric].iloc[i]+0.15,df[y_metric].iloc[i]+0.15),xytext=(df[x_metric].iloc[i]+0.15,df[y_metric].iloc[i]+0.15))
    plt.xlabel(xlabel,size=15)
    plt.ylabel(ylabel,size=15)

    plt.subplot(1,2,2)
    sns.scatterplot(data=df,x=x_metric,y=y_metric,hue='City')
    for i in range(len(df['ZipCode'])):
        plt.annotate(str(df['ZipCode'].iloc[i]),xy=(df[x_metric].iloc[i]+0.15,df[y_metric].iloc[i]+0.15),xytext=(df[x_metric].iloc[i]+0.15,df[y_metric].iloc[i]+0.15))
    plt.xlabel(xlabel,size=15)
    plt.ylabel(ylabel,size=15)

    plt.show()
    
def uni_barplot(df,col):
    plt.bar(df[col],col)
    plt.show()