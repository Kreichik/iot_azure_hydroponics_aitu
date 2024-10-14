import streamlit as st
import pandas as pd
import plotly.express as px
from azure.storage.blob import BlobServiceClient
from io import StringIO
import datetime
import time
import plotly.graph_objects as go

import os

# Настройки подключения к Azure
connection_string = st.secrets['connectionstring']
container_name = "iotcontainer"


# Функция для получения CSV данных из Blob Storage
def get_csv_from_blob(blob_service_client, container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    csv_str = blob_data.decode('utf-8')
    data = pd.read_csv(StringIO(csv_str), delimiter=';')
    return data

# Подключение к Blob Storage



# Чтение и объединение всех CSV файлов

i=0
def create_gauge(temp):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = temp,
        title = {'text': "Температура от датчика BLE"},
        gauge = {
            'bar': {'color': "rgba(0,0,0,0)"},  # Прозрачный цвет для полосы
            'axis': {'range': [-20, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'steps': [
                {'range': [-20, 0], 'color': "red"},
                {'range': [0, 25], 'color': "green"},
                {'range': [25, 50], 'color': "orange"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 1,
                'value': temp}}))

    return fig

# Проверка, что данные загружены
def main():
    i=0

    bar_temp = st.empty()
    chart_temp = st.empty()

    while True:

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        now = datetime.datetime.now(datetime.timezone.utc)

        # Формируем шаблон для папок текущего часа
        # path_to_files = f"d1test/year={now.year}/month={now.month:02}/day={now.day:02}/hour={now.hour:02}"
        path_to_files = f"d1test/year={now.year}/month={now.month:02}/day={now.day:02}"

        os.write(1, path_to_files.encode('utf-8'))
        # Получение списка файлов в директории за текущий час
        os.write(1, b'collect blob\n')
        blob_list = blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=path_to_files)
        os.write(1, b'collected bob\n')

        # Список для хранения всех данных
        all_data = pd.DataFrame()

        for blob in blob_list:
            os.write(1, b'Startinf blob loop\n')
            if blob.name.endswith('.csv'):
                data = get_csv_from_blob(blob_service_client, container_name, blob.name)
                all_data = pd.concat([all_data, data])

        refresh_interval = 1

        if all_data.empty:
            st.write("Нет данных для отображения.")
        else:
            # Преобразование времени в формат datetime
            all_data['EventProcessedUtcTime'] = pd.to_datetime(all_data['EventProcessedUtcTime'])

            # Фильтрация данных по текущему часу
            #all_data = all_data[all_data['EventProcessedUtcTime'].dt.hour == now.hour]
            all_data = all_data[all_data['EventProcessedUtcTime'].dt.hour == now.hour]
            # Отображение данных в виде графиков
            #st.write("Данные загружены, строим графики за текущий день...")
            i = i + 3
            # График для температуры
            all_data_sorted = all_data.sort_values(by='EventProcessedUtcTime', ascending=False)

            # Получаем последнее значение температуры
            last_temperature = all_data_sorted.iloc[0]['Temperature']
            fig = create_gauge(last_temperature)


            fig_temp = px.line(all_data, x="EventProcessedUtcTime", y="Temperature", title="Температура за текущий день")
            #st.plotly_chart(fig_temp, key=i+3)
            chart_temp.plotly_chart(fig_temp, key=f'temperature_{i}')
            #os.write(1, str(i).encode('utf-8'))
            bar_temp.plotly_chart(fig, key=f'temperature_bar_{i}')

            # График для влажности
            # fig_humidity = px.line(all_data, x="EventProcessedUtcTime", y="Humidity", title="Влажность за текущий день")
            # st.plotly_chart(fig_humidity, key=i+)
        time.sleep(refresh_interval)


if __name__ == '__main__':
    main()
