from random import sample
import pandas as pd
import datetime as dt
import numpy as np
import scipy.special
from bokeh.layouts import row, column
from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
import math

def histogram_log_return(df, bins):
    #establish min and max pct returns, 
    min = math.floor((df['log_returns'].min())*100)/100
    max = math.ceil((df['log_returns'].max())*100)/100

    #create incrementation of pct_returns from min to max establish the left and right for histogram
    increments = np.arange(min, max+.01 ,abs(min-max)/bins)
    left = increments[0:-1]
    right = increments[1:]
    frequency = [np.nan]*len(left)
    df_hist = {'frequency':frequency, 'left':left, 'right':right}
    df_hist = pd.DataFrame.from_dict(df_hist)

    #count frequency number that lies in bin range
    for i in range(len(df_hist)):
        l = df_hist['left'][i]
        r = df_hist['right'][i]
        count = df.loc[df['log_returns'] > l]
        count = count.loc[count['log_returns'] < r]
        df_hist['frequency'][i] = len(count)

    return df_hist