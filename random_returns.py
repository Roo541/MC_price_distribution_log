import numpy as np
import pandas as pd
import datetime as dt

def return_list_generator(df):
    random_list = []
    for i in range(len(df)):
        alpha = df['return'][i]
        for j in range(int(df['frequency'][i])):
            random_list.append(alpha)

    return random_list