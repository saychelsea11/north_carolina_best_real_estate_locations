import pandas as pd
import numpy as np

def add_price_metrics(df):
    #Creating new variables representing price increases from 2006 and 2012, respectively, to June 2017
    df['PriceIncrease'] = df['Price2017'] - df['Price2012']
    df['PriceIncreasePerc'] = ((df['Price2017'] - df['Price2012'])/df['Price2012'])*100
    df['PriceIncreaseYearly'] = df['PriceIncrease']/5
    return df

def return_on_investment(df,years):
    #Calculating the future housing price taking into consideration the initial 2017 price and the yearly price appreciation
    df['FutureHousingPrice'] = df['Price2017'] + years*df['PriceIncreaseYearly']
    
    #Calculating the return on investment using initial purchase price, rental revenue and final housing price
    df['ReturnOnInvestment'] = df['FutureHousingPrice'] - df['Price2017']
    
    #Calculating rate of return by dividing total return over a given period by the initial purchase price
    df['RateOfReturn'] = (df['ReturnOnInvestment']/df['Price2017'])*100
    return df
