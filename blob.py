import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from azure.storage.blob import BlobServiceClient
from io import StringIO
import datetime
import time

# Azure Storage connection settings
connection_string = st.secrets['connectionstring']
container_name = "iotcontainer"

# Function to fetch CSV data from Azure Blob Storage
def get_csv_from_blob(blob_service_client, container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    csv_str = blob_data.decode('utf-8')
    data = pd.read_csv(StringIO(csv_str), delimiter=';')
    return data

# Fetch data from Azure Blob Storage
def fetch_blob_data():
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    now = datetime.datetime.now(datetime.timezone.utc)
    path_to_files = f"d1test/year={now.year}/month={now.month:02}/day={now.day:02}"

    blob_list = blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=path_to_files)
    all_data = pd.DataFrame()

    for blob in blob_list:
        if blob.name.endswith('.csv'):
            data = get_csv_from_blob(blob_service_client, container_name, blob.name)
            all_data = pd.concat([all_data, data])
    
    return all_data

# Fetch the data (this will reload each time the page refreshes)
all_data = fetch_blob_data()

# Ensure data is loaded
if not all_data.empty:
    st.title('IoT Data Dashboard')
    
    # Convert timestamp column to datetime (if exists in your data)
    if 'EventProcessedUtcTime' in all_data.columns:
        all_data['EventProcessedUtcTime'] = pd.to_datetime(all_data['EventProcessedUtcTime'])

    # Set up the 2x2 grid for the charts
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    # Chart 1: Time Series (Temperature or any metric over time)
    with col1:
        fig1 = px.line(all_data, x='EventProcessedUtcTime', y='Temperature', 
                        title='Temperature Over Time', 
                        line_shape='linear')
        # Update the trace color to red
        fig1.update_traces(line=dict(color='red'))
        st.plotly_chart(fig1, use_container_width=True, key="chart1")

    # Chart 2: Histogram (Temperature Distribution)
    with col2:
        fig2 = px.histogram(all_data, x='Temperature', title='Temperature Distribution')
        st.plotly_chart(fig2, use_container_width=True, key="chart2")

    # Chart 3: Scatter plot (Temperature vs Humidity)
    with col3:
        fig1 = px.line(all_data, x='EventProcessedUtcTime', y='Humidity', 
                        title='Humidity Over Time', 
                        line_shape='linear')
        # Update the trace color to red
        fig1.update_traces(line=dict(color='blue'))
        st.plotly_chart(fig1, use_container_width=True, key="chart3")

    # Chart 4: Gauge (Current Temperature)
    with col4:
        current_temp = all_data['Temperature'].iloc[-1] if 'Temperature' in all_data.columns else 0
        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_temp,
            title={'text': "Current Temperature"},
            gauge={'axis': {'range': [None, 50]}, 'bar': {'color': "green"}}))
        st.plotly_chart(fig4, use_container_width=True, key="chart4")

else:
    st.warning("No data available to display.")

# Auto-refresh the page every 60 seconds
refresh_interval = 1  # Set the refresh interval in seconds
time.sleep(refresh_interval)
st.rerun()

