import streamlit as st
import pandas as pd
import plotly.express as px
from azure.storage.blob import BlobServiceClient
from io import StringIO
from datetime import datetime

# Настройки подключения к Azure
connection_string = st.secrets['connectionstring']
container_name = "iotcontainer"

# Функция для получения CSV данных из Blob Storage
def get_csv_from_blob(blob_service_client, container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    csv_str = blob_data.decode('utf-8')
    data = pd.read_csv(StringIO(csv_str), delimiter=';')  # Чтение CSV с разделителем ;
    return data

# Подключение к Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Получаем текущую дату и час
now = datetime.utcnow()

# Формируем шаблон для папок текущего часа
path_to_files = f"d1test/year={now.year}/month={now.month:02}/day={now.day:02}/hour={now.hour:02}"

# Получение списка файлов в директории за текущий час
blob_list = blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=path_to_files)

# Список для хранения всех данных
all_data = pd.DataFrame()

# Чтение и объединение всех CSV файлов
for blob in blob_list:
    if blob.name.endswith('.csv'):
        data = get_csv_from_blob(blob_service_client, container_name, blob.name)
        all_data = pd.concat([all_data, data])

# Проверка, что данные загружены
if all_data.empty:
    st.write("Нет данных для отображения.")
else:
    # Преобразование времени в формат datetime
    all_data['EventProcessedUtcTime'] = pd.to_datetime(all_data['EventProcessedUtcTime'])

    # Фильтрация данных по текущему часу
    all_data = all_data[all_data['EventProcessedUtcTime'].dt.hour == now.hour]

    # Отображение данных в виде графиков
    st.write("Данные загружены, строим графики за текущий час...")

    # График для температуры
    fig_temp = px.line(all_data, x="EventProcessedUtcTime", y="Temperature", title="Температура за текущий час")
    st.plotly_chart(fig_temp)

    # График для влажности
    fig_humidity = px.line(all_data, x="EventProcessedUtcTime", y="Humidity", title="Влажность за текущий час")
    st.plotly_chart(fig_humidity)
