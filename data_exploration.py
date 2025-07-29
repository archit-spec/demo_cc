#!/usr/bin/env python3
"""Quick data structure analysis"""

import pandas as pd
import numpy as np

df = pd.read_csv('finalapi.csv')
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nData types:")
print(df.dtypes)
print("\nSample data:")
print(df.head())
print("\nMissing values (showing 99999 as well):")
print((df == 99999).sum())