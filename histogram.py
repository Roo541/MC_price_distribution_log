from random import sample
import pandas as pd
import datetime as dt
import numpy as np
import scipy.special
from bokeh.layouts import row, column
from bokeh.plotting import figure, show
from bokeh.models import DatetimeTickFormatter
import math
from scipy.stats import norm 

def mc_histogram(df, bins):
    #establish min and max pct returns, 
    min = math.floor((df['return_output_price'].min())*100)/100
    max = math.ceil((df['return_output_price'].max())*100)/100

    #create incrementation of pct_returns from min to max establish the left and right for histogram
    increments = np.arange(min, max+.01 ,abs(min-max)/bins)
    left = increments[0:-1]
    right = increments[1:]
    frequency = [np.nan]*len(left)
    df_freq = {'frequency':frequency, 'left':left, 'right':right}
    df_freq = pd.DataFrame.from_dict(df_freq)

    #count the frequency for histogram bin range
    for i in range(len(df_freq)):
        l = df_freq['left'][i]
        r = df_freq['right'][i]
        count = df.loc[df['return_output_price'] > l]
        count = count.loc[count['return_output_price'] < r]
        df_freq['frequency'][i] = len(count)

    #plot 
    p = figure(plot_height = 800, plot_width = 1500, 
            title = '{} Daily Pct Returns'.format('DIS'),
            x_axis_label = 'Forecast Price', 
            y_axis_label = 'Frequency')

    # Add a quad glyph
    p.quad(bottom=0, top=df_freq['frequency'], 
        left=df_freq['left'], right=df_freq['right'], 
        fill_color='orange', line_color='black')

    # Show the plot
    show(p)
    return