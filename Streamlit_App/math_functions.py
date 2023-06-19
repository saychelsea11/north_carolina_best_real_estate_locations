import pandas as pd
import numpy as np

def add_price_metrics(df,timespan):
    #Calculating approximate number of years from the timespan entered by the user
    years = np.round((timespan[1] - timespan[0]).days/365)
    
    #Creating new variables representing price increases from the start date to end date entered by the user
    df['PriceIncrease($)'] = df['EndPrice($)'] - df['StartPrice($)']
    df['PriceIncreasePerc(%)'] = ((df['EndPrice($)'] - df['StartPrice($)'])/df['StartPrice($)'])*100
    df['PriceIncreaseYearly($)'] = df['PriceIncrease($)']/years
    return df

def return_on_investment(df,years):
    #Calculating the future housing price taking into consideration the initial 2017 price and the yearly price appreciation
    df['FutureHousingPrice($)'] = df['EndPrice($)'] + years*df['PriceIncreaseYearly($)']
    
    #Calculating the return on investment using initial purchase price, rental revenue and final housing price
    df['ReturnOnInvestment($)'] = df['FutureHousingPrice($)'] - df['EndPrice($)']
    
    print (df[['City','ReturnOnInvestment($)']].groupby('City').agg(['count','mean','median','std','sum'])['ReturnOnInvestment($)'].sort_values('mean',ascending=False),'/n')
    print (df[['County','ReturnOnInvestment($)']].groupby('County').agg(['count','mean','median','std','sum'])['ReturnOnInvestment($)'].sort_values('mean',ascending=False))
    
    return df
    
def rate_of_return(df,years):
    #Calculating rate of return by dividing total return over a given period by the initial purchase price
    df['RateOfReturn(%)'] = (df['ReturnOnInvestment($)']/df['EndPrice($)'])*100
    
    print (df[['City','RateOfReturn(%)']].groupby('City').agg(['count','mean','median','std','sum'])['RateOfReturn(%)'].sort_values('mean',ascending=False),'/n')
    print (df[['County','RateOfReturn(%)']].groupby('County').agg(['count','mean','median','std','sum'])['RateOfReturn(%)'].sort_values('mean',ascending=False))
    
    return df

def agg_by_city(df,var,sort_by_val):
    data = df[['City',var]].groupby('City').agg(['count','mean','median','std','max','min','sum']).round(2)[var].sort_values(sort_by_val,ascending=False)
    data_state = df[['State',var]].groupby('State').agg(['count','mean','median','std','max','min','sum']).round(2)[var].sort_values(sort_by_val,ascending=False)
    data = pd.concat([data,data_state])
    data = data.drop('index',axis=1)
    
    print (data)
    
    return data

def agg_by_county(df,var,sort_by_val):
    data = df[['County',var]].groupby('County').agg(['count','mean','median','std','max','min','sum']).round(2)[var].sort_values(sort_by_val,ascending=False)
    data_state = df[['State',var]].groupby('State').agg(['count','mean','median','std','max','min','sum']).round(2)[var].sort_values(sort_by_val,ascending=False)
    data = data.append(data_state)
    data = data.drop('index',axis=1)
    
    print (data)
    
    return data
