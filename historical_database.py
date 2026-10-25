import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
db_url= os.getenv("database_url")
conn=psycopg2.connect(db_url)
cursor=conn.cursor()
create_table_query="""
CREATE TABLE IF NOT EXISTS weather_data (
    city VARCHAR(50),
    latitude DECIMAL(8,5),
    longitude DECIMAL(8,5),
    date DATE,
    temperature_2m_mean DECIMAL(5,2),
    precipitation_sum DECIMAL(5,2),
    PRIMARY KEY (city, date)   -- ensures one row per city per date
);
"""
cursor.execute(create_table_query)
conn.commit()
cursor.close()
conn.close()
print("Table created succssfully")
