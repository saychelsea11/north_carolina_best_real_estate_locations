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
    xytick_size = 30
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
            xytext=(df.index[i]+100,df[y_metric].iloc[i]+anno_dist),size=anno_size,alpha=0.6)
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
            xytext=(df.index[i]+100,df[y_metric].iloc[i]+anno_dist),size=anno_size,alpha=0.6)
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
    
def uni_barplot(df,metric_choice,xlabel,ylabel,title,plot_label=''):
    plt.bar(df[metric_choice].index,df[metric_choice].values,alpha=0.5,label=plot_label)
    plt.title(title,size=25)
    plt.xticks(size=20,rotation=45)
    plt.yticks(size=20)
    plt.xlabel(xlabel,size=25)
    plt.ylabel(ylabel,size=25)
    plt.legend(fontsize="15",markerscale=1)
    
def bi_barplot(df1,df2,metric_choice,xlabel,ylabel,title,plot_label=[]):
    plt.bar(df1[metric_choice].index,df1[metric_choice].values,alpha=0.5,label=plot_label[0])
    plt.bar(df2[metric_choice].index,df2[metric_choice].values,alpha=0.5,label=plot_label[1])
    plt.title(title,size=25)
    plt.xticks(size=20,rotation=45)
    plt.yticks(size=20)
    plt.xlabel(xlabel,size=25)
    plt.ylabel(ylabel,size=25)
    plt.legend(fontsize="15",markerscale=1)
    
def adj_barplot(df1,df2,metric,xlabel,ylabel,title,plot_labels=[]):
    x = np.arange(df1.shape[0])
    plt.bar(x + 0.2, df1[metric].values, alpha=0.5, label=plot_labels[0], width=0.4)
    plt.bar(x - 0.2, df2[metric].values, alpha=0.5, label=plot_labels[1], width=0.4)
    plt.title(title,size=25)
    plt.xticks(x, df1[metric].index, size=20,rotation=45)
    plt.yticks(size=20)
    plt.xlabel(xlabel,size=25)
    plt.ylabel(ylabel,size=25)
    plt.legend(fontsize="15",markerscale=1)
    
def uni_lineplot(df,xlabel,ylabel,title,chart_label=''):
    plt.plot(df,label=chart_label,linewidth = '10',alpha=0.7)
    plt.title(title,size=50)
    plt.xticks(size=30)
    plt.yticks(size=30)
    plt.xlabel(xlabel,size=45)
    plt.ylabel(ylabel,size=45)
    plt.legend(fontsize="40",markerscale=10)

def historical_timeseries_grid(df):    
    states = ['CA','TX','FL','NY','PA','IL','OH','GA','NC']
    
    for chart in range(1,10):
        df_state = df.copy()
        df_state = df_state[df_state['State']==states[chart-1]]
        df_timeseries_mean = df_state.mean(numeric_only=True)
        df_timeseries_median = df_state.median(numeric_only=True)
        df_timeseries_mean.index = pd.to_datetime(df_timeseries_mean.index)
        df_timeseries_median.index = pd.to_datetime(df_timeseries_median.index)
        
        plt.subplot(3,3,chart)
        plt.plot(df_timeseries_mean,label='Mean',linewidth = '10',alpha=0.7)
        plt.plot(df_timeseries_median,label='Median',linewidth = '10',alpha=0.7)
        plt.title(f'Mean and Median Historical Housing Prices',size=50)
        plt.xticks(size=30)
        plt.yticks(size=30)
        plt.xlabel('Timeline',size=45)
        plt.ylabel('Housing Price($)',size=45)
        plt.legend(fontsize="40",markerscale=10)
    
