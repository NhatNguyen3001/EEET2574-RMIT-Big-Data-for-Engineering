import requests
from datetime import datetime, timedelta
import time
import json
import boto3

api_key = "c7c7e288398ae157212c5a7cbd9beb8b"


def log_message(message):
    current_time_utc = datetime.utcnow()
    current_time_local = current_time_utc + timedelta(hours=7)  # Adjusted for UTC+7
    formatted_time = current_time_local.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{formatted_time}] {message}")


def flatten_dict(weather_data, city): 
    # Extracting relevant information from the 'hourly' data
    hourly_data = weather_data.get("hourly", [])
    hourly_extracted_data = []

    for hour_data in hourly_data:
        dt_hourly = datetime.utcfromtimestamp(hour_data.get("dt", None)).strftime('%Y-%m-%d %H:%M:%S')
        temp_hourly = hour_data.get("temp", None)
        pressure_hourly = hour_data.get("pressure", None)
        humidity_hourly = hour_data.get("humidity", None)
        wind_speed_hourly = hour_data.get("wind_speed", None)
        weather_description_hourly = hour_data.get("weather", [{}])[0].get("description", None) 

        hourly_extracted_data.append({
            "DateTime": dt_hourly,
            "Temperature": temp_hourly,
            "Pressure": pressure_hourly,
            "Humidity": humidity_hourly,
            "Wind Speed": wind_speed_hourly,
            "Weather Description": weather_description_hourly,
        })
    # Organize the extracted information into a dictionary
    extracted_data = {
        "city": city,
        "lon": lon,
        "lat": lat,
        "hourly_data": hourly_extracted_data
    }

    # Convert the dictionary to a JSON-formatted string
    json_data = json.dumps(extracted_data, indent=2)

    # Print or use the JSON-formatted string
    return json_data

def fetch_lat_lon(city):
    try:
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        if data:
            entry = data[0]
            lat, lon = entry.get("lat"), entry.get("lon")
            return lat, lon

        else:
            print(f"No data found for {city}.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None, None


def put_record_to_kinesis(stream_names, record_data):
    try:
        kinesis = boto3.client('kinesis', region_name='us-east-1')
        # Put the record into the Kinesis stream
        response = kinesis.put_record(
            StreamName=stream_names,
            Data=json.dumps(record_data),
            PartitionKey='city'
        )
        sequence_number = response['SequenceNumber']
        shard_id = response['ShardId']
        log_message(f"Record put into Kinesis. Shard ID: {shard_id}, SequenceNumber: {sequence_number}")
    except Exception as e:
        log_message(f"Error fetching weather data for {city}: {e}")

def fetch_and_put_data(city, lat, lon, last_retrieval_time):
    try:
        url_weather = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely%2Cdaily%2Calerts&appid={api_key}"
            
        response_weather = requests.get(url_weather)
        response_weather.raise_for_status()  # Raise an HTTPError for bad responses
        data_weather = response_weather.json()

        flattened_data = flatten_dict(data_weather, city)
      

        # Check if one minute has passed since the last retrieval
        if last_retrieval_time is None or (datetime.utcnow() - last_retrieval_time) >= timedelta(minutes=1):
            log_message(f"{city}: {flattened_data}")
            put_record_to_kinesis('weather-stream', flattened_data)
            return datetime.utcnow()  # Update the last retrieval time

        
    except requests.exceptions.RequestException as e:
        log_message(f"Error fetching weather data for {city}: {e}")

    return last_retrieval_time

cities = ['San Diego', 'San Francisco', 'Los Angeles', 'San Antonio', 'Dallas', 'Houston', 'Chicago', 'Minneapolis', 'Indianapolis', 'Charlotte']
coordinates = {}  # Dictionary to store city coordinates

# Fetch coordinates for each city (run only once)
for city in cities:
    lat, lon = fetch_lat_lon(city)
    coordinates[city] = (lat, lon)

# Use the stored coordinates in subsequent runs
last_retrieval_times = {city: None for city in cities}

while True:
    for city in cities:
        lat, lon = coordinates[city]
        last_retrieval_times[city] = fetch_and_put_data(city, lat, lon, last_retrieval_times[city])

    # Pause for one minute before the next iteration
    log_message("Waiting for next predictor in next 60 minutes...")    
    time.sleep(60*60)
