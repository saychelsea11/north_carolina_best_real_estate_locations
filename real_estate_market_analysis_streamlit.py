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

from bs4 import BeautifulSoup
import geopy
from geopy.geocoders import Nominatim
from math_functions import *
from wrangling_functions import *
from plotting_functions import *
from data_extraction_functions import *

path = r'C:\Users\sdas\Github_DS\north_carolina_best_real_estate_locations\Datasets\Zip_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv'
df_zillow = pd.read_csv(path)
df_zillow.head()

st.write("""
## U.S. Real Estate Market Analysis
""")

state_choice = st.selectbox('Select state:', sorted(df_zillow['State'].unique()))
df_zillow = df_zillow[df_zillow['State']==state_choice]

fig3 = plt.figure(constrained_layout=True,figsize=(21,11))
plt.hist(df_zillow['2022-12-31'])
st.pyplot(fig3)

#st.write(df_zillow)

