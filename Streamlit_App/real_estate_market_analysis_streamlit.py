import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import requests
import json
import streamlit as st
from datetime import datetime
from bs4 import BeautifulSoup
import geopy
from geopy.geocoders import Nominatim
from math_functions import *
from wrangling_functions import *
from plotting_functions import *
from data_extraction_functions import *

path = r'C:\Users\sdas\Github_DS\north_carolina_best_real_estate_locations\Datasets\Zip_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'
df_zillow = pd.read_csv(path)

st.write("""
## U.S. Real Estate Market Analysis
- Enter the **state** and **cities** within that state
- Select the historical **timespan** to analyze, based on which future returns will be projected
- Then enter the number of **years** to project returns for
- Lastly, select the analysis **scope** and **metric**
""")

#User input for state
state_choice = st.selectbox('Select state', sorted(pd.Series(df_zillow['State'].unique()).dropna()))
df_zillow = df_zillow[df_zillow['State']==state_choice]

#User input for cities
city_choice = st.multiselect('Select cities', sorted(pd.Series(df_zillow['City'].unique()).dropna()))

#Creating slider for date range user input
timespan = st.slider(
    "Select historical analysis timeline",
    value=(datetime(2000, 1, 1, 9, 30),datetime(2022, 12, 1, 9, 30)),
    format="YYYY-MM")

#User input for number of years to project returns for
future_timespan = st.number_input("Enter number of years to project returns")
future_timespan = int(future_timespan)
    
#User input for city/county analysis
#city_county_choice = st.selectbox('Select analysis scope', ['City','County'])
city_county_choice = st.radio("Select analysis scope", options=["City", "County"])

#User input for aggregate metric
#metric_choice = st.selectbox('Select price analysis metric', ['Mean','Median'])
metric_choice = st.radio("Select analysis metric", options=["Mean", "Median"])
metric_choice = metric_choice.lower()

#Button to start analysis based on the user inputs
if st.button('Enter'):
    #Cleaning and wrangling dataset
    df_zillow = filter_data_pipeline(df_zillow,city_col_name="City",state_col_name="State",
                    cols=['RegionName','City','State','CountyName','SizeRank'],
                    start_date=str(pd.to_datetime(timespan[0]).to_period('m')),end_date=str(pd.to_datetime(timespan[1]).to_period('m')),
                    cities=city_choice,
                    states=[])
                    
    #Adding price metrics
    df_zillow = add_price_metrics(df_zillow,timespan)

    if city_county_choice=="City":
        fig3 = plt.figure(constrained_layout=True,figsize=(21,15))
        
        plt.subplot(2,2,1)
        #Aggregate by city - price
        data = agg_by_city(df_zillow,'EndPrice',metric_choice)
        uni_barplot(data,metric_choice,'City','Price($)')
        
        plt.subplot(2,2,2)
        #Aggregate by city - price increase percentage
        data = agg_by_city(df_zillow,'PriceIncreasePerc',metric_choice)
        uni_barplot(data,metric_choice,'City','Price Increase (%)')
        
        plt.subplot(2,2,3)
        #Aggregate by city - return on investment
        df_zillow = return_on_investment(df_zillow,future_timespan)
        data = agg_by_city(df_zillow,'ReturnOnInvestment',metric_choice)
        uni_barplot(data,metric_choice,'City','Return on Investment ($)')
        
        plt.subplot(2,2,4)
        #Aggregate by city - rate of return
        df_zillow = rate_of_return(df_zillow,future_timespan)
        data = agg_by_city(df_zillow,'RateOfReturn',metric_choice)
        uni_barplot(data,metric_choice,'City','Rate of Retun (%)')
        
        st.pyplot(fig3)
    else: 
        #Aggregate by county - price
        data = agg_by_county(df_zillow,'EndPrice',metric_choice)
        uni_barplot(data,metric_choice,'County','Price($)')

        #Aggregate by county - price increase percentage
        data = agg_by_county(df_zillow,'PriceIncreasePerc',metric_choice)
        uni_barplot(data,metric_choice,'County','Price Increase (%)')
        
        #Aggregate by city - return on investment
        df_zillow = return_on_investment(df_zillow,future_timespan)
        data = agg_by_county(df_zillow,'ReturnOnInvestment',metric_choice)
        uni_barplot(data,metric_choice,'County','Return on Investment ($)')
        
        #Aggregate by city - rate of return
        df_zillow = rate_of_return(df_zillow,future_timespan)
        data = agg_by_county(df_zillow,'RateOfReturn',metric_choice)
        uni_barplot(data,metric_choice,'County','Rate of Retun (%)')
    
    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'EndPrice','Avg Housing Price Across Zipcodes on ' + str(timespan[1].date()),
                    'Avg Housing price ($)',city_county_choice)
    
    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'PriceIncreasePerc','Avg Yearly Housing Price Increase Percent Across Zipcodes on ' + str(timespan[1].date()),
                    'Housing price increase per year (%)',city_county_choice)

    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'ReturnOnInvestment','Avg Return On Investment Across Zipcodes after ' + str(future_timespan) + 'Years',
                    'Total return on investment ($)',city_county_choice)

    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'RateOfReturn','Avg Rate of Return Across Zipcodes after ' + str(future_timespan) + 'Years',
                    'Total rate of return (%)',city_county_choice)
else: 
    pass

