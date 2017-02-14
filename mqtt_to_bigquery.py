import ast
import uuid
import json
import datetime
from ConfigParser import SafeConfigParser
import paho.mqtt.client as mqtt
from googleapiclient import errors
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def config_read():
    parser = SafeConfigParser()
    parser.read('mqtt.conf')
    return parser


def gcp_service(api_name):
    try:
        credentials = GoogleCredentials.get_application_default()
        return discovery.build(api_name, 'v2', credentials=credentials)
    except:
        print "GCP promise undefined. Please Login."


def stream_data(project_id, dataset_id, table_name, row, suffix=None, num_retries=5):
    insert_all_data = {
        'rows': [{
            'json': row,
            'insertId': str(uuid.uuid4()),
        }]
    }

    if suffix is not None:
        insert_all_data['templateSuffix'] = suffix

    bigquery = gcp_service('bigquery')
    if bigquery is not None:
        bigquery.tabledata().insertAll(projectId=project_id,
                                       datasetId=dataset_id,
                                       tableId=table_name,
                                       body=insert_all_data).execute(num_retries=num_retries)
        print('[{}] Loaded 1 row into {}:{}'.format(row['date'], dataset_id, table_name))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    topic = config_read().get('mqtt_broker', 'topic')
    client.subscribe(topic)


def on_message(client, userdata, msg):
    message = ast.literal_eval(msg.payload)
    try:
        project_id = config_read().get('gcp', 'project_id')
        dataset_id = config_read().get('gcp', 'dataset_id')
        table_name = config_read().get('gcp', 'table_name')
        message['topic'] = msg.topic
        date_suffix = None
        if config_read().getboolean('gcp', 'templatesuffix'):
            date = str(json.loads(msg.payload)['date'])
            date_suffix = "_" + datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y%m%d")
        stream_data(project_id, dataset_id, table_name, message, suffix=date_suffix)
    except errors.HttpError, e:
        print "[ERROR] %s" % json.loads(e.content)['error']['message']


def main():
    broker_ip = config_read().get('mqtt_broker', 'ip')
    broker_port = config_read().getint('mqtt_broker', 'port')
    broker_timeout = config_read().getint('mqtt_broker', 'timeout')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_ip, broker_port, broker_timeout)
    client.loop_forever()


if __name__ == '__main__':
    main()
