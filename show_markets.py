#!/usr/bin/env python

import os
import pandas as pd

filename_mk_btc = 'markets_btc.csv'
df_markets = pd.read_csv(os.path.join(os.path.dirname(__file__), filename_mk_btc), sep=';')
print(df_markets)