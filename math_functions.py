import pandas as pd
import numpy as np

def add_price_metrics(df,years):
    #Creating new variables representing price increases from 2006 and 2012, respectively, to June 2017
    df['PriceIncrease'] = df['EndPrice'] - df['StartPrice']
    df['PriceIncreasePerc'] = ((df['EndPrice'] - df['StartPrice'])/df['StartPrice'])*100
    df['PriceIncreaseYearly'] = df['PriceIncrease']/years
    return df

def return_on_investment(df,years):
    #Calculating the future housing price taking into consideration the initial 2017 price and the yearly price appreciation
    df['FutureHousingPrice'] = df['EndPrice'] + years*df['PriceIncreaseYearly']
    
    #Calculating the return on investment using initial purchase price, rental revenue and final housing price
    df['ReturnOnInvestment'] = df['FutureHousingPrice'] - df['EndPrice']
    
    print (df[['City','ReturnOnInvestment']].groupby('City').agg(['count','mean','median','std','sum'])['ReturnOnInvestment'].sort_values('mean'),'/n')
    print (df[['County','ReturnOnInvestment']].groupby('County').agg(['count','mean','median','std','sum'])['ReturnOnInvestment'].sort_values('mean'))
    
    return df
    
def rate_of_return(df,years):
    #Calculating rate of return by dividing total return over a given period by the initial purchase price
    df['RateOfReturn'] = (df['ReturnOnInvestment']/df['EndPrice'])*100
    
    print (df[['City','RateOfReturn']].groupby('City').agg(['count','mean','median','std','sum'])['RateOfReturn'].sort_values('mean'),'/n')
    print (df[['County','RateOfReturn']].groupby('County').agg(['count','mean','median','std','sum'])['RateOfReturn'].sort_values('mean'))
    
    return df

def agg_by_city(df,var):
    print (df[['City',var]].groupby('City').agg(['mean','median','std','max','min','sum','count']).round(2)[var].sort_values('mean',ascending=False))

def agg_by_county(df,var):
    print (df[['County',var]].groupby('County').agg(['mean','median','std','max','min','sum','count']).round(2)[var].sort_values('mean',ascending=False))