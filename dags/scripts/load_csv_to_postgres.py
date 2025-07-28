import os
import psycopg2
import pandas as pd
import math

DB_CONFIG = {
    'host': 'postgres',
    'database': 'nyc_trips',
    'user': 'airflow',
    'password': 'airflow'
}

DATA_FOLDER = '/opt/airflow/data/yellow_tripdata_2019' 
CHUNKSIZE = 100_000

def load_csv_to_postgres():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loaded_files (
            filename TEXT PRIMARY KEY
        )
    """)
    conn.commit()

    cursor.execute("SELECT filename FROM loaded_files")
    processed_files = {row[0] for row in cursor.fetchall()}

    for filename in sorted(os.listdir(DATA_FOLDER)):
        if not filename.endswith('.csv') or filename in processed_files:
            continue

        csv_path = os.path.join(DATA_FOLDER, filename)
        print(f"Processing file: {csv_path}")

        total_rows = sum(1 for _ in open(csv_path)) - 1
        num_batches = math.ceil(total_rows / CHUNKSIZE)
        print(f"Total rows: {total_rows}, Batches: {num_batches}")

        for chunk in pd.read_csv(csv_path, chunksize=CHUNKSIZE):
            chunk = chunk.rename(columns={
                'VendorID': 'vendor_id',
                'tpep_pickup_datetime': 'tpep_pickup_datetime',
                'tpep_dropoff_datetime': 'tpep_dropoff_datetime',
                'passenger_count': 'passenger_count',
                'trip_distance': 'trip_distance',
                'total_amount': 'total_amount'
            })
            
            chunk = chunk.dropna()
            chunk['amount_per_passenger'] = chunk['total_amount'] / chunk['passenger_count']

            for _, row in chunk.iterrows():
                cursor.execute("""
                    INSERT INTO raw_trips (
                        vendor_id, tpep_pickup_datetime, tpep_dropoff_datetime, 
                        passenger_count, trip_distance, total_amount, amount_per_passenger
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['vendor_id'], row['tpep_pickup_datetime'], row['tpep_dropoff_datetime'],
                    row['passenger_count'], row['trip_distance'], row['total_amount'], row['amount_per_passenger']
                ))
            conn.commit()
            print(f"Inserted {CHUNKSIZE} rows from {filename}.")

      
        cursor.execute("INSERT INTO loaded_files (filename) VALUES (%s)", (filename,))
        conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_csv_to_postgres()