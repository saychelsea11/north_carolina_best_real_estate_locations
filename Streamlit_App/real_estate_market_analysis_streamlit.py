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
df_zillow_timeseries = df_zillow.drop(['RegionID','RegionName','City','State','Metro','CountyName','SizeRank'],axis=1)
df_zillow_timeseries_mean = df_zillow_timeseries.mean()
df_zillow_timeseries_median = df_zillow_timeseries.median()
df_zillow_timeseries_mean.index = pd.to_datetime(df_zillow_timeseries_mean.index)
df_zillow_timeseries_median.index = pd.to_datetime(df_zillow_timeseries_median.index)

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
    years = np.round((timespan[1] - timespan[0]).days/365)
    df_zillow = add_price_metrics(df_zillow,timespan)
    
    #Plotting historical average housing prices
    st.write("")
    st.write("")
    st.write(f'### Historical Housing Price Trend in {state_choice}')
    
    fig3 = plt.figure(figsize=(36,25))
    uni_lineplot(df_zillow_timeseries_mean,'Timeline','Avg Housing Price($)',f'Mean and Median Historical Housing Price in {state_choice}','Mean')
    uni_lineplot(df_zillow_timeseries_median,'Timeline','Avg Housing Price($)',f'Mean and Median Historical Housing Price in {state_choice}','Median')
    st.pyplot(fig3)
    
    st.write("")
    st.write("")
    st.write(f'### Analyzing Average Housing Price Trends Across Cities in {state_choice}')

    if city_county_choice=="City":
        fig3 = plt.figure(constrained_layout=True,figsize=(21,15))
        
        plt.subplot(2,2,1)
        #Aggregate by city - price
        data_end_price = agg_by_city(df_zillow,'EndPrice',metric_choice)
        data_start_price = agg_by_city(df_zillow,'StartPrice',metric_choice)
        adj_barplot(data_start_price,data_end_price,metric_choice,'City','Avg price($)','Avg Historical Housing Price',
                    ['Price on ' + str(timespan[0].date()), 'Price on ' + str(timespan[1].date())])
        
        plt.subplot(2,2,2)
        #Aggregate by city - price increase percentage
        data = agg_by_city(df_zillow,'PriceIncreasePerc',metric_choice)
        uni_barplot(data,metric_choice,'City','Avg price increase(%)','Avg Historical Housing Price Increase %')
        
        plt.subplot(2,2,3)
        #Aggregate by city - return on investment
        df_zillow = return_on_investment(df_zillow,future_timespan)
        data = agg_by_city(df_zillow,'ReturnOnInvestment',metric_choice)
        uni_barplot(data,metric_choice,'City','Avg ROI($)','Avg Return On Investment ' + str(future_timespan) + ' Years after ' + str(timespan[1].date()))
        
        plt.subplot(2,2,4)
        #Aggregate by city - rate of return
        df_zillow = rate_of_return(df_zillow,future_timespan)
        data = agg_by_city(df_zillow,'RateOfReturn',metric_choice)
        uni_barplot(data,metric_choice,'City','Avg ROR(%)','Avg Rate of Return ' + str(future_timespan) + ' Years after ' + str(timespan[1].date()))
        
        st.pyplot(fig3)
    else: 
        #Aggregate by county - price
        data_end_price = agg_by_city(df_zillow,'EndPrice',metric_choice)
        data_start_price = agg_by_city(df_zillow,'StartPrice',metric_choice)
        adj_barplot(data_start_price,data_end_price,metric_choice,'County','Avg price($)','Avg Historical Housing Price',
                    ['Price on ' + str(timespan[0].date()), 'Price on ' + str(timespan[1].date())])

        #Aggregate by county - price increase percentage
        data = agg_by_county(df_zillow,'PriceIncreasePerc',metric_choice)
        uni_barplot(data,metric_choice,'County','Avg price increase(%)','Avg Historical Housing Price Increase %')
        
        #Aggregate by city - return on investment
        df_zillow = return_on_investment(df_zillow,future_timespan)
        data = agg_by_county(df_zillow,'ReturnOnInvestment',metric_choice)
        uni_barplot(data,metric_choice,'County','Avg ROI($)','Avg Return On Investment after ' + str(future_timespan) + ' Years')
        
        #Aggregate by city - rate of return
        df_zillow = rate_of_return(df_zillow,future_timespan)
        data = agg_by_county(df_zillow,'RateOfReturn',metric_choice)
        uni_barplot(data,metric_choice,'County','Avg ROR(%)','Avg Rate of Return after ' + str(future_timespan) + ' Years')
    
    #Comparison by zip code - price increase percentage
    st.write("")
    st.write("")
    st.write(f'### Analyzing historical housing price trends across zipcodes and cities in {state_choice}')
    uni_scatterplot(df_zillow,'EndPrice','Avg Housing Price Across Zipcodes on ' + str(timespan[1].date()),
                    'Avg housing price ($)',city_county_choice)
    
    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'PriceIncreasePerc','Avg Housing Price Increase Percent Across Zipcodes on ' + str(timespan[1].date()),
                    'Avg housing price increase(%)',city_county_choice)
    
    st.write("")
    st.write("")
    st.write(f'### Forecasting returns on housing investments across zipcodes and cities in {state_choice}')
    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'ReturnOnInvestment','Avg Return On Investment Across Zipcodes after ' + str(future_timespan) + ' Years',
                    'Avg return on investment ($)',city_county_choice)

    #Comparison by zip code - price increase percentage
    uni_scatterplot(df_zillow,'RateOfReturn','Avg Rate of Return Across Zipcodes after ' + str(future_timespan) + ' Years',
                    'Avg rate of return (%)',city_county_choice)
else: 
    pass

