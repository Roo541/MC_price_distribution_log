import numpy as np
import pandas as pd 

def sample_mean(df):
    summation = 0.00
    for i in range(len(df)):
        summation += df['return_output_price'][i]
    mu = summation/(len(df)-1)
    return mu

def sample_var(df,mu):
    summation = 0.00
    for i in range(len(df)):
        summation += (df['return_output_price'][i] - mu)**2
    sigma2 = summation/(len(df)-1)
    return sigma2

def sample_skewness(df,mu, sigma2):
    summation = 0.00
    for i in range(len(df)):
        summation += (df['return_output_price'][i] - mu)**3
    skewness = summation/(len(df)*np.sqrt(sigma2)*sigma2)
    return skewness

def sample_kurtosis(df,mu, sigma2):
    summation = 0.00
    for i in range(len(df)):
        summation += (df['return_output_price'][i] - mu)**4
    kurtosis = summation/(len(df)*sigma2**2)
    return kurtosis