import psycopg2

DB_CONFIG = {
    'host': 'postgres',
    'database': 'nyc_trips',
    'user': 'airflow',
    'password': 'airflow'
}

def transform_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM raw_trips
        WHERE vendor_id IS NULL
           OR tpep_pickup_datetime IS NULL
           OR tpep_dropoff_datetime IS NULL
           OR passenger_count IS NULL
           OR total_amount IS NULL;
    """)
    conn.commit()


    cursor.execute("""
        UPDATE raw_trips
        SET amount_per_passenger = CASE
            WHEN passenger_count > 0 THEN total_amount / passenger_count
            ELSE total_amount
        END;
    """)
    conn.commit()

    cursor.close()
    conn.close()
    print("Transformation completed.")

if __name__ == "__main__":
    transform_data()