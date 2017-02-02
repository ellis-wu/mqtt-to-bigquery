# MQTT to BigQuery
MQTT subscriber message streaming load into BigQuery.

## How to use

### Step 1
Download this repositories to your localhost:
```sh
$ git clone https://github.com/ellisMing/mqtt-to-bigquery.git
$ cd mqtt-to-bigquery
```

### Step 2
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

### Step 3
Build your docker image:
```sh
$ docker build -t <your name>/<image name>:<version> .
```

### Step 4
Run your docker image:
```sh
$ docker run -dti --name mqtt2bq <your name>/<image name>:<version>
```

### Step 5
Your can see docker container logs:
```sh
$ docker logs mqtt2bq
Connected with result code 0
GCP promise undefined. Please Login.
```

Your must login with your Google Cloud Platform authentication:
```sh
$ docker exec -ti mqtt2bq gcloud init

...

$ docker exec -ti mqtt2bq gcloud beta auth application-default login

...

```

Check your authentication success:
```sh
$ docker logs mqtt2bq
[2017-02-02 16:12:03.967857] Loaded 1 row into mqtt_daily:data
```
