__author__ = 'skv'

import pandas as pd
from pandas_datareader import data as pdr

def get_data(symbol, start_dt, end_dt, multi_year=False, minute=False):
    df = pdr.get_data_yahoo(symbol, start_dt, end_dt)

    return df

