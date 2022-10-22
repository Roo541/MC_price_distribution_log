import histogram_df as histogram
import sample_parameters as sample
import method_of_moment as mom
import datetime as dt
import numpy as np
import pandas as pd
import random_returns as rand_list
import random
import histogram as hgram
import time 
import scipy.optimize
import eod_ohlc_pull as eod

def data_pull(start, end, symbol):
    df = eod.ohlc(start, end, symbol)

    df = pd.DataFrame.from_dict(df)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    df = df[['date', 'adjusted_close']]

    df = df.sort_values(by='date', ascending=True)
    df = df.reset_index(drop=True)
    return df

def mc_check(ticker, results):
    #Form dataframe 
    start = '2020-09-09'
    end = '2022-09-09'
    df = data_pull(start, end, ticker)
    
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    df['log_returns'] = [np.nan]*len(df)

    #create log returns
    for i in range(1,len(df)):
        df['log_returns'][i] = np.log(df['adjusted_close'][i]/df['adjusted_close'][i-1])

    bins = 100
    df_freq = histogram.histogram_log_return(df, bins)
    df_freq['mid_return'] = [np.nan]*len(df_freq)

    for i in range(len(df_freq)):
        df_freq['mid_return'][i] = (df_freq['left'][i] + df_freq['right'][i])/2.0

    #create df of returns and frequency making the bins for us to put our mc results in
    random_returns = {'frequency':[], 'return':[]}
    for i in range(len(df_freq)):
        if df_freq['frequency'][i] >= 1:
            random_returns['frequency'].append(df_freq['frequency'][i])
            random_returns['return'].append(df_freq['mid_return'][i])

    random_returns = pd.DataFrame.from_dict(random_returns)
    returns_list = rand_list.return_list_generator(random_returns)

    #9/30/22,94.330002
    # in general get last day
    s_0 = df['adjusted_close'][len(df)-1]
    simulation_prices = {'return_output_price':[]}
    #outer Monte Carlo define the days of projection
    t_days = 30
    for i in range(int(1e5)):
        # the days of returns
        sum_return = 0.00
        for j in range(t_days):
            #choose a random return from weighted log return box
            value = random.choice(returns_list)
            sum_return += value
        #exponential function to sum up all total returns and calculate final price at end of t_days
        s_1 = s_0*np.exp(sum_return)
        #appending to projected price of sum log returns
        simulation_prices['return_output_price'].append(s_1)

    simulation_prices = pd.DataFrame.from_dict(simulation_prices)

    mu_hat = sample.sample_mean(simulation_prices)
    sigma2_hat = sample.sample_var(simulation_prices, mu_hat)
    sigma_hat = np.sqrt(sigma2_hat)
    skewness_hat = sample.sample_skewness(simulation_prices, mu_hat, sigma2_hat)
    kurtosis_hat = sample.sample_kurtosis(simulation_prices, mu_hat, sigma2_hat)

    zGuess = np.array([1,1,1])
    z = scipy.optimize.fsolve(mom.MyFunction, zGuess, args=(mu_hat, sigma2_hat, skewness_hat))
    mu_theo = z[0]
    sigma_theo = z[1]
    sigma2_theo = sigma_theo**2
    skew_theo = z[2]

    price_final = data_pull('2022-10-21', '2022-10-21', ticker)
    price_final = price_final['adjusted_close'][0]

    results['ticker'].append(ticker)
    results['price_initial'].append(s_0)
    results['price_final'].append(price_final)
    results['mu_sample'].append(mu_hat)
    results['sigma2_sample'].append(sigma2_hat)
    results['sigma_sample'].append(sigma_hat)
    results['mu_theo'].append(mu_theo)
    results['sigma2_theo'].append(sigma2_theo)
    results['sigma_theo'].append(sigma_theo)
    return results

tickers = ['DIS', 'AMZN', 'AAPL', 'TMO', 'QRVO']
results = {'ticker':[], 'price_initial':[], 'price_final':[], 'mu_sample':[], 'sigma2_sample':[], 'sigma_sample':[], 'mu_theo':[], 'sigma2_theo':[], 'sigma_theo':[]}

for i in tickers:
    mc_check(i, results)

final_results = pd.DataFrame.from_dict(results)
print(final_results)

