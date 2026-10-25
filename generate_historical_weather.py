import requests
import json
import pandas as pd
import os 
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

cities_coords={
    "delhi": (28.61, 77.23),
    "mumbai":(19.07, 72.88),
    "lucknow":(26.85, 80.95),
    "jaipur":(26.91, 75.79),
    "ujjain":(23.18, 75.79),
    "mysuru":(12.30, 76.64)
}
all_dfs=[]
for city,(latitude,longitude) in cities_coords.items():
    url="https://archive-api.open-meteo.com/v1/archive"
    params={
        "latitude":latitude,
        "longitude":longitude,
        'daily': "temperature_2m_mean,precipitation_sum",
        "timezone":"auto",
        "start_date":"2025-10-01",
        "end_date":"2026-10-01"
    }
    response = requests.get(url, params=params)
    data=response.json()
    city_df=pd.DataFrame(data['daily'])
    city_df["city"]=city
    city_df["latitude"]=latitude
    city_df["longitude"]=longitude
    all_dfs.append(city_df)
final_df = pd.concat(all_dfs,ignore_index=True)
final_df.rename(columns={"time":"date"},inplace=True)
final_df['date']=pd.to_datetime(final_df['date'])
list_1=['city', 'latitude', 'longitude', 'date', 'temperature_2m_mean', 'precipitation_sum']
final_df=final_df[list_1]
rows=[]
for row in final_df.itertuples(index=False, name=None):
    rows.append(row)

load_dotenv()
db_url=os.getenv('database_url')
conn=psycopg2.connect(db_url)
cursor=conn.cursor()
execute_values(cursor,
"""
INSERT INTO weather_data(city,
    latitude ,
    longitude,
    date,
    temperature_2m_mean,
    precipitation_sum) values %s
    on conflict(city,date) DO UPDATE 
    SET 
    temperature_2m_mean=EXCLUDED.temperature_2m_mean,
    precipitation_sum=EXCLUDED.precipitation_sum
""",
rows)
conn.commit()
cursor.close()
conn.close()  
