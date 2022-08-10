#%% 
from datetime import datetime
from pydoc import locate
from turtle import title
import matplotlib.pyplot as plt
from meteostat import Point, Daily,Monthly
from numpy import size
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

import numpy as np
import statsmodels.api as sm

title_text_font = {'size':'20','weight':'normal','fontname':'Segoe UI'}
label_text_font = {'size':'18','weight':'normal','fontname':'Segoe UI'}

# Set time period
start = datetime(1950, 1, 1)
end = datetime(2022, 8, 1)

# Create Point for Vancouver, BC
issaquah    = 47.55116221960466, -121.99327046596636
seattle     = 47.60628689373281, -122.32973467198013
sanfan      = 37.77816773810975, -122.44165278156379
london      = 51.70952600638239, -0.2639768922644242
newyork     = 40.71351021324743, -73.99610272821182
shanghai    = 31.331588357783843, 121.49524836991638
beijing     = 40.010877318390314, 116.39239367867765
melbourne   = -37.75459158938347, 144.84264433167704
iceland     =  64.14598471604364, -21.934811248761466
oslo        = 59.91311086504237, 10.75637502289596
stockholm   = 59.329619903822, 18.07801440635025
copenhagen  = 55.69149175900506, 12.644677769460486
anchorage   = 61.21740323143628, -149.89431987389762
santiago    = -33.34816745829232, -70.63334119541513
rio_gallegos = -51.62338802715795, -69.21867406384987
boston      = 42.35578888191694, -71.03811162035355

print('location done')

#%% define functions
def get_monthly_data(location):
    location = Point(*location)

    data = Monthly(location, start, end)
    data = data.fetch()

    # extend data
    import pandas as pd
    years       = pd.DatetimeIndex(data.index.values).year
    data.insert(7,'year',years,allow_duplicates=True)

    # calculate yearly avg
    data_avg = data[data['year']<2022].groupby('year').mean()
    return data,data_avg

def get_daily_data(location):
    location = Point(*location)

    data = Daily(location, start, end)
    data = data.fetch()

    # extend data
    import pandas as pd
    years       = pd.DatetimeIndex(data.index.values).year
    data.insert(7,'year',years,allow_duplicates=True)

    # calculate yearly avg
    data_avg = data[data['year']<2022].groupby('year').mean()
    return data,data_avg

def plot_raw_data(location,location_str):
    monthly_data,_ = get_daily_data(location)
    ax = monthly_data.plot(y=['tmax'],figsize=(17,7))
    ax.set_title(f'{location_str} Daily Max Temperature in Celsius',**title_text_font)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    plt.box(False)
    plt.show()

# Plot line chart including average, minimum and maximum temperature
def plot_avg(location,location_str):
    _,data_avg = get_daily_data(location)

    plt.figure(figsize=(30,15))
    lowess      = sm.nonparametric.lowess
    yearly_avg  = data_avg['tmax'].tolist()
    x           = data_avg.index.values
    z           = lowess(yearly_avg,x,frac=1./6)[:,1]

    data_avg['year'] = data_avg.index

    # plot monthly max temperature 
    ax = data_avg.plot(y=['tmax'],figsize=(17,7))
    # plot lowess line 
    ax.plot(x,z,linewidth=4)

    #ax.grid(False)
    plt.box(False)
    ax.set_title(f"{location_str} Annual Mean of Daily Max Temperature in Celsius",**title_text_font)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    ax.legend(['Yearly AVG','Lowess Regression'], ncol=2, loc='upper left')
    #ax.set_ylim([0,30])
    plt.show()

#%% 
plot_raw_data(seattle,'Seattle')
plot_avg(seattle,"Seattle")


#%%
plot_raw_data(anchorage,"Alask Anchorage")
plot_avg(anchorage,"Alask Anchorage")

#%%
plot_avg(oslo,"Oslo")

#%%
plot_raw_data(boston,"Boston")
plot_avg(boston,"Boston")
