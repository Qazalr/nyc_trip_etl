import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.load_csv_to_postgres import load_csv_to_postgres
from scripts.transform_trips import transform_data
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='nyc_trip_etl',
    default_args=default_args,
    description='ETL pipeline for NYC Taxi data every 5 minutes',
    schedule='*/5 * * * *', 
    start_date=datetime(2025, 7, 1),
    catchup=False,
) as dag:

    extract_load_task = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    extract_load_task >> transform_task