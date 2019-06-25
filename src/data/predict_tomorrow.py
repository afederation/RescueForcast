

#%% Imports
import pandas as pd
import numpy as np
import re
import datetime
import random

#%% Fast.ai functions
def add_datepart(df, fldname, drop=True, time=False, errors="raise"):
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64

    if not np.issubdtype(fld_dtype, np.datetime64):
        df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True, errors=errors)
    targ_pre = re.sub('[Dd]ate$', '', fldname)
    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    if time: attr = attr + ['Hour', 'Minute', 'Second']
    for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())
    df[targ_pre + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
    if drop: df.drop(fldname, axis=1, inplace=True)

#%% My Functions
def add_holiday_info(df):
    import pandas.tseries.holiday as hol

    us_cal = hol.USFederalHolidayCalendar()
    dr = pd.date_range(start='2019-01-01', end='2020-01-01')
    us_holidays = us_cal.holidays(start=dr.min(), end=dr.max())
    
    df['holiday'] = 0
    df['date'] =  pd.to_datetime(data['date'], infer_datetime_format=True,
                                  format='datetime64[ns]')
    df['holiday'] = data.date.isin(us_holidays)
    
    # Insert the number of days before and after closest holiday
    holiday = df.holiday
    since = []
    d = 0
    for i in range(len(holiday)):
        d += 1
        if holiday[i]:
            d = 0   # if it's a holiday, reset
        since.append(d)
    #data['holiday_days_since'] = since
    
    before = []
    d = 0
    for i in range(len(holiday)):
        d += 1
        if holiday[len(holiday) - (i+1)]:
            d = 0   # if it's a holiday, reset
        before.append(d)
    #data['holiday_days_before'] = before

    df['holiday_closest'] = np.minimum(since, before)

def add_google_trend(df):
    '''
    Adds google trend data for hiking topic in King County
    No current API for getting real-time data
    Using data from 2018 as a surrogate for now
    '''
      
    raw_filepath = '../../data/raw/'  
    trends = pd.read_csv(f'{raw_filepath}googletrends_hiking.csv', header=None, names=['date_t', 'trend'])  
    trends['date_t'] =  pd.to_datetime(trends['date_t'], infer_datetime_format=True,
                              format='datetime64[ns]')  
    df = pd.merge(data, trends, how='outer', left_on='DATE', right_on='date_t')

#%% Define the day, extract date variables
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
year_ago = datetime.datetime.today() - datetime.timedelta(days=364)

# load the 2019 calendar
date_range = pd.date_range(start='1/1/2019', end='1/1/2020')


data = pd.DataFrame([date_range]).T
data.columns = ['date']
add_datepart(data, 'date', drop=False)
add_holiday_info(data)

#%%
add_google_trend(data)








#%% Yesterday's Results
yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
mission = 0
pred = random.random()*.4 + .1
rounded_pred = round(pred, 2)