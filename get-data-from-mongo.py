import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
try:
    mongo_client = MongoClient("mongodb+srv://m001-student:s3cret@cluster0.xyr2yuj.mongodb.net/?retryWrites=true&w=majority")
    database_name = "weather_db"
    collection_name = "weather_collection"
    db = mongo_client[database_name]
    collection = db[collection_name]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Query all documents from the collection
try:
    cursor = collection.find({})
except Exception as e:
    print(f"Error querying MongoDB collection: {e}")
    exit()

# Extract data from MongoDB cursor
data_list = []
for document in cursor:
    try:
        city = document.get("city", "")
        hourly_data = document.get("hourly_data", [])

        for hourly_entry in hourly_data:
            data_list.append({
                "DateTime": hourly_entry.get("DateTime", ""),
                "City": city,
                "Temperature": hourly_entry.get("Temperature", ""),
                "Pressure": hourly_entry.get("Pressure", ""),
                "Humidity": hourly_entry.get("Humidity", ""),
                "Wind Speed": hourly_entry.get("Wind Speed", ""),
                "Weather Description": hourly_entry.get("Weather Description", "")
            })
    except Exception as e:
        print(f"Error processing document: {e}")

# Create a DataFrame from the list of dictionaries
try:
    df = pd.DataFrame(data_list)
except Exception as e:
    print(f"Error creating DataFrame: {e}")
    exit()

# Convert 'DateTime' column to datetime type
try:
    df['DateTime'] = pd.to_datetime(df['DateTime'])
except Exception as e:
    print(f"Error converting 'DateTime' column to datetime type: {e}")
    exit()

# Display the DataFrame
print(df)
