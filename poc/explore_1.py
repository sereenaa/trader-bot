import pandas as pd 
import numpy as np
import csv
import datetime

anz_df = pd.read_csv('ANZ.AX.csv')
cba_df = pd.read_csv('CBA.AX.csv')
nab_df = pd.read_csv('NAB.AX.csv')

anz_df = anz_df.dropna()
cba_df = cba_df.dropna()
nab_df = nab_df.dropna()

anz_df['day_of_week'] = anz_df.apply(lambda row: datetime.datetime.strptime(row.Date, '%Y-%m-%d').strftime('%A'), axis = 1)
cba_df['day_of_week'] = cba_df.apply(lambda row: datetime.datetime.strptime(row.Date, '%Y-%m-%d').strftime('%A'), axis = 1)
nab_df['day_of_week'] = nab_df.apply(lambda row: datetime.datetime.strptime(row.Date, '%Y-%m-%d').strftime('%A'), axis = 1)


anz_fri_df = anz_df[anz_df['day_of_week'].str.match('Friday')]
anz_fri_df = pd.DataFrame(anz_fri_df, columns = ['Open', 'Close'])

