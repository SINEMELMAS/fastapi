import pandas as pd
import sqlite3

df = pd.read_csv(r'C:\Users\Vostro\Desktop\Machine Failure Prediction using Sensor data.csv')

conn = sqlite3.connect('machine_data.db')
df.to_sql('machines', conn, if_exists='replace', index=False)
conn.close()

