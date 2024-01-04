import requests
import azure.functions as func
import os
from azure.eventhub import EventHubProducerClient, EventData

def main(mytimer: func.TimerRequest):
    mbta_url = 'https://api-v3.mbta.com/vehicles'
    response = requests.get(mbta_url)

    if response.status_code == 200:
        data = response.json()

        # Initialize Event Hub client
        connection_str = os.environ['EVENT_HUB_CONN_STR']
        event_hub_name = os.environ['EVENT_HUB_NAME']
        client = EventHubProducerClient.from_connection_string(connection_str, event_hub_name)

        # Send data to Event Hub
        with client:
            event_data_batch = client.create_batch()
            event_data_batch.add(EventData(str(data)))
            client.send_batch(event_data_batch)
