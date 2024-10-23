import pandas as pd
import sqlite3

df = pd.read_csv(r'C:\Users\Vostro\Desktop\Machine Failure Prediction using Sensor data.csv')

conn = sqlite3.connect('Machine.db')
df.to_sql('Machine', conn, if_exists='replace', index=False)
conn.close()

