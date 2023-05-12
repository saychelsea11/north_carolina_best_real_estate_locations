import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_neighborhoods_and_coordinates(df):
    plt.figure(figsize=(30,12))
    plt.scatter(df['longitude'],df['latitude'],alpha=0.5)
    for i in df.index:
      plt.annotate(df['neighborhood'].iloc[i],xy=(df['longitude'].iloc[i],df['latitude'].iloc[i]),xytext=(df['longitude'].iloc[i],df['latitude'].iloc[i]))
    plt.xlabel('Longitude',size=15)
    plt.ylabel('Latitude',size=15)
    plt.title('Mapping of neighborhood names and coordinates',size=20)
    plt.show()

def uni_scatterplot(df,y_metric,title,ylabel,city_county_choice):
    #Function used to create a univariate (1 variable) plot for a provided variable in the dataset
    #Inputs: dataframe, column name in dataframe, y-axis label
    #fig3 = plt.figure(constrained_layout=True,figsize=(36,10))
    title_size = 50
    xylabel_size = 45
    xytick_size = 25
    marker_size = 800
    anno_size = 30
    anno_dist_factor = 0.005
    
    #Calculating annotation distance from data range and distance factor
    y_metric_range = np.max(df[y_metric]) - np.min(df[y_metric])
    anno_dist = anno_dist_factor * y_metric_range
    
    #Plotting section
    fig3 = plt.figure(figsize=(36,30))
    
    if city_county_choice=="City":
        sns.scatterplot(data=df,x=df.index,y=y_metric,hue='City',s=marker_size,alpha=1)
        for i in range(len(df['ZipCode'])):
            plt.annotate(str(df['ZipCode'].iloc[i]),xy=(df.index[i]+100,df[y_metric].iloc[i]+anno_dist),
            xytext=(df.index[i]+100,df[y_metric].iloc[i]+anno_dist),size=anno_size,color='black',alpha=0.5)
        plt.title(title,size=title_size)
        plt.xlabel('Zip code',size=xylabel_size)
        plt.ylabel(ylabel,size=xylabel_size)
        plt.xticks(size=xytick_size)
        plt.yticks(size=xytick_size)
        plt.legend(fontsize="30",markerscale=5)
    else:
        sns.scatterplot(data=df,x=df.index,y=y_metric,hue='County',s=marker_size,alpha=1)
        for i in range(len(df['ZipCode'])):
            plt.annotate(str(df['ZipCode'].iloc[i]),xy=(df.index[i]+100,df[y_metric].iloc[i]+anno_dist),
            xytext=(df.index[i]+100,df[y_metric].iloc[i]+anno_dist),size=anno_size)
        plt.title(title,size=title_size)
        plt.xlabel('Zip code',size=xylabel_size)
        plt.ylabel(ylabel,size=xylabel_size)
        plt.xticks(size=xytick_size)
        plt.yticks(size=xytick_size)
        plt.legend(fontsize="30",markerscale=5)

    st.pyplot(fig3)

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
    
def uni_barplot(df,metric_choice,xlabel,ylabel):
    #fig3 = plt.figure(constrained_layout=True,figsize=(21,11))
    plt.bar(df[metric_choice].index,df[metric_choice].values,alpha=0.5)
    plt.xticks(size=20,rotation=45)
    plt.yticks(size=20)
    plt.xlabel(xlabel,size=25)
    plt.ylabel(ylabel,size=25)
    
    #st.pyplot(fig3)