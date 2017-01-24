# MQTT to BigQuery
MQTT subscriber message streaming load into BigQuery.

## How to use
Change your parameter in `mqtt.conf`:
```sh
[mqtt_broker]
ip=[YOUR BROKER IP]
port=[YOUR BROKER PORT]
timeout=60

[gcp]
project_id = [YOUR GCP PROJECT ID]
dataset_id = [YOUR BIGQUERY DATASET ID]
table_name = [YOUR BIGQUERY TABLE ID]
templatesuffix = false
```

* __templatesuffix__:
  * If set `ture`, treats the destination table as a base template, and inserts the rows into an instance table named "{destination}_{YYYYMMDD}".
  * Your subscriber message must have `date` key, because templatesuffix inserts an instance table using `date` key.
  * If your want change table suffix style, you must modify `mqtt_to_bigquery.py`.
