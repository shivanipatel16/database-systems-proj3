import numpy as np
import pandas as pd

df = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv')

df.drop(['CRASH DATE', 'CRASH TIME', 'ZIP CODE', 'ON STREET NAME', 'LATITUDE', 'LONGITUDE', 'LOCATION', 'CROSS STREET NAME',
              'OFF STREET NAME', 'CONTRIBUTING FACTOR VEHICLE 3',
              'CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5', 'COLLISION_ID', 'VEHICLE TYPE CODE 1',
              'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4',
              'VEHICLE TYPE CODE 5'], axis=1, inplace=True)


"""
columns left = ['BOROUGH', 'NUMBER OF PERSONS INJURED',
       'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
       'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
       'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
       'NUMBER OF MOTORIST KILLED', 'CONTRIBUTING FACTOR VEHICLE 1',
       'CONTRIBUTING FACTOR VEHICLE 2']
"""

df.dropna(inplace=True)
df = df[df['CONTRIBUTING FACTOR VEHICLE 1'].str.contains('Unspecified') == False]
df = df[df['CONTRIBUTING FACTOR VEHICLE 2'].str.contains('Unspecified') == False]

numerical_columns = ['NUMBER OF PERSONS INJURED',
       'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED',
       'NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST INJURED',
       'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED',
       'NUMBER OF MOTORIST KILLED']
for c in numerical_columns:
    df[c[10:]] = np.where(df[c] != 0, True, False)
df.drop(numerical_columns, axis=1, inplace=True)


columns = ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2']
for c in columns:
    new_columns = set(df[c])
    for new_c in new_columns:
        df[str(str(new_c) + " - " + str(c))] = np.where(df[c] == new_c, True, False)

df.drop(columns, axis=1, inplace=True)
print(df.columns)
print(len(df.columns))
print(df.head)

df.to_csv('INTEGRATED-DATASET.csv', header=True, index=False, columns=list(df.axes[1]))