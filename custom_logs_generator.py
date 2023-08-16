import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import random
import datetime

# Number of log entries to generate
num_entries = 100

# Generate random log data
log_data = []
for _ in range(num_entries):
    timestamp = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
    ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    user_agent = f"UserAgent-{random.randint(1, 100)}"
    log_data.append((timestamp, ip_address, user_agent))

# Create a DataFrame
df = pd.DataFrame(log_data, columns=["timestamp", "ip_address", "user_agent"])

# Define Parquet schema
parquet_schema = pa.schema([
    ("timestamp", pa.timestamp("ns")),  # Use "ns" for nanoseconds
    ("ip_address", pa.string()),
    ("user_agent", pa.string())
])

# Convert DataFrame to Arrow Table
table = pa.Table.from_pandas(df, schema=parquet_schema)

# Generate a unique timestamp for filenames
unique_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Define the log directory
log_directory = "/var/log/random_logs"
os.makedirs(log_directory, exist_ok=True)

# Write to Parquet file
parquet_output_path = os.path.join(log_directory, f"random_logs_{unique_timestamp}.parquet")
pq.write_table(table, parquet_output_path)

print(f"Generated {num_entries} log entries and saved Parquet to '{parquet_output_path}'.")

# Read the Parquet file
parquet_file_path = parquet_output_path
table = pq.read_table(parquet_file_path)

# Convert the table data to a readable text format
text_data = ""
for col in table.schema.names:
    text_data += f"{col}: {table[col].to_pandas().tolist()}\n"

# Save the text data to a text file
text_output_path = os.path.join(log_directory, f"random_logs_{unique_timestamp}.txt")
with open(text_output_path, "w") as text_file:
    text_file.write(text_data)

print(f"Converted Parquet data to ASCII and saved to '{text_output_path}'.")
