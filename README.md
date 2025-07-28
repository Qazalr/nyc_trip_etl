# NYC Taxi Trip ETL Pipeline 🗽🚕

This project demonstrates an ETL pipeline using **Apache Airflow + Docker** to process and transform New York City yellow taxi trip data for 2019.

---

## 📦 Dataset

We use the **Yellow Taxi Trip Records for 2019**.

📂 **Dataset Source:**  
[Kaggle - NYC Yellow Taxi 2019 Dataset](https://www.kaggle.com/code/dhruvildave/starter-new-york-city-taxi-trips?select=yellow_tripdata_2019)

⬇️ After downloading, place the `.csv` files inside: /opt/airflow/data/yellow_tripdata_2019/

---

## 🛠️ Setup Instructions

### 🔧 Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

### 🚀 Step-by-Step

1. **Clone the repository**

```bash
git clone https://github.com/Qazalr/nyc_trip_etl.git
cd nyc_trip_etl

**Download Airflow Docker Compose template**
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.3/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

**start airflow**
docker-compose up

**Access Airflow UI**

Go to: http://localhost:8080
	•	Username: airflow
	•	Password: airflow



🧠 DAGs Overview
	•	nyc_trip_etl_dag.py: Main DAG for managing the pipeline.
	•	load_csv_to_postgres.py: Loads and cleans CSV files into PostgreSQL.
	•	transform_trips.py: Applies transformations (e.g., amount_per_passenger column).

**PostgreSQL Access**

to access run 
docker exec -it nyc_trip_etl-postgres-1 psql -U airflow -d nyc_trips
Then you can run:
SELECT COUNT(*) FROM raw_trips;
SELECT * FROM raw_trips LIMIT 10;

Notes
	•	Data is inserted in chunks to avoid memory overflow.
	•	Files already loaded are tracked in the loaded_files table.
	•	Rows with null values are removed.
	•	New column amount_per_passenger is added during transformation.

⸻
🛑 Shutting Down

To stop all containers:

docker-compose down