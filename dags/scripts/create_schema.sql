
\c nyc_trips;

DROP TABLE IF EXISTS raw_trips;
CREATE TABLE raw_trips (
    vendor_id INT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance FLOAT,
    ratecode_id INT,
    store_and_fwd_flag VARCHAR(5),
    pu_location_id INT,
    do_location_id INT,
    payment_type INT,
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    improvement_surcharge FLOAT,
    total_amount FLOAT,
    congestion_surcharge FLOAT
);