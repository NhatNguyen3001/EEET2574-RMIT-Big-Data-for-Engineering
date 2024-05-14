import boto3
import json
from pymongo import MongoClient
from datetime import datetime, timedelta



# Create a MongoDB client
mongo_client = MongoClient("mongodb+srv://m001-student:s3cret@cluster0.xyr2yuj.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection string
database_name = "weather_db"
collection_name = "weather_collection"
db = mongo_client[database_name]
collection = db[collection_name]

# Create a Kinesis client
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
kinesis_stream_name = "weather-stream"

# Get the shard iterator for TRIM_HORIZON
response = kinesis_client.describe_stream(StreamName=kinesis_stream_name)
shard_id = response['StreamDescription']['Shards'][1]['ShardId']  # Assuming there is at least one shard
shard_iterator_response = kinesis_client.get_shard_iterator(
    StreamName=kinesis_stream_name,
    ShardId=shard_id,
    ShardIteratorType='TRIM_HORIZON'
)

shard_iterator = shard_iterator_response['ShardIterator']

def log_message(message):
    current_time_utc = datetime.utcnow()
    current_time_local = current_time_utc + timedelta(hours=7)  # Adjusted for UTC+7
    formatted_time = current_time_local.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{formatted_time}] {message}")

while True:
    records_response = kinesis_client.get_records(ShardIterator=shard_iterator, Limit=1000)
    records = records_response['Records']

    for record in records:
        if len(record) > 0:
            data = record['Data']
            sequence_number = record['SequenceNumber']
            try:
                # Attempt to load data as JSON
                
                json_data  = json.loads(json.loads(data))
                json_data['_id'] = sequence_number
            
                # Check if document with the same _id exists
                existing_doc = collection.find_one({'_id': sequence_number})

                if existing_doc:
                    # Document with the same _id already exists, decide what to do
                    log_message(f"Document with _id {sequence_number} already exists. Skipping...")
                else:
                    # Save the record to MongoDB
                    collection.insert_one(json_data)
                    log_message(f"Record with Sequence Number {sequence_number} added to MongoDB")
                
                log_message("Waiting for next events...")

            except json.JSONDecodeError as e:
                log_message(f"Error decoding JSON: {e}")
                continue  # Skip to the next record if JSON decoding fails        

    shard_iterator = records_response['NextShardIterator']
