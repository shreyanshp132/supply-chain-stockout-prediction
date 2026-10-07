import requests
import json
import pandas as pd

cities_coords={
    "delhi": (28.61, 77.23),
    "mumbai":(19.07, 72.88),
    "lucknow":(26.85, 72.88),
    "jaipur":(26.91, 75.79),
    "ujjain":(23.18, 75.79),
    "mysuru":(12.30, 76.64)
}
all_dfs=[]
for city,(lattitude,longitude) in cities_coords.items():
    url="https://archive-api.open-meteo.com/v1/archive"
    params={
        "latitude":lattitude,
        "longitude":longitude,
        'daily': "temperature_2m_mean,precipitation_sum",
        "timezone":"auto",
        "start_date":"2025-10-01",
        "end_date":"2026-10-01"
    }
    response = requests.get(url, params=params)
    data=response.json()
    df=pd.DataFrame(data['daily'])
    df["city"]=city
    all_dfs.append(df)
final_df = pd.concat(all_dfs,ignore_index=True)
print(final_df)
