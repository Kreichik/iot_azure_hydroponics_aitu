import streamlit as st
import pandas as pd
import plotly.express as px
from azure.storage.blob import BlobServiceClient
from io import StringIO
import datetime
import time
import plotly.graph_objects as go

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

# Функция для создания индикатора в виде полукруга
def create_gauge(temp, text, range, color_line):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temp,
        title={'text': text},
        gauge={
            'bar': {'color': color_line},  # Прозрачный цвет для полосы
            'axis': {'range': range, 'tickwidth': 1, 'tickcolor': "darkblue"},
            'steps': [
                {'range': [-20, 0], 'color': "red"},
                {'range': [0, 25], 'color': "green"},
                {'range': [25, 50], 'color': "orange"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 1,
                'value': temp}}))
    return fig

# Основная функция для отображения данных
def main():
    i = 0
    st.title('IoT Data Dashboard')

    # Создание двух строк для размещения элементов
    gauge_col1, gauge_col2 = st.columns(2)  # Первая строка для шкал
    graph_col1, graph_col2 = st.columns(2)  # Вторая строка для графиков

    bar_temp1 = gauge_col1.empty()
    bar_temp2 = gauge_col2.empty()
    chart_temp1 = graph_col1.empty()
    chart_temp2 = graph_col2.empty()


    while True:

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        now = datetime.datetime.now(datetime.timezone.utc)
        path_to_files = f"d1test/year={now.year}/month={now.month:02}/day={now.day:02}"
        blob_list = blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=path_to_files)

        all_data = pd.DataFrame()

        for blob in blob_list:
            if blob.name.endswith('.csv'):
                data = get_csv_from_blob(blob_service_client, container_name, blob.name)
                all_data = pd.concat([all_data, data])

        refresh_interval = 1

        if all_data.empty:
            st.write("Нет данных для отображения.")
        else:
            all_data['EventProcessedUtcTime'] = pd.to_datetime(all_data['EventProcessedUtcTime'])
            all_data = all_data[all_data['EventProcessedUtcTime'].dt.day == now.day]

            i += 1
            all_data_sorted = all_data.sort_values(by='EventProcessedUtcTime', ascending=False)

            # Получаем последнее значение температуры для шкалы
            last_temperature = all_data_sorted.iloc[0]['Temperature']
            fig_gauge1 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=current_temp,
                title={'text': "Current Temperature"},
                gauge={'axis': {'range': [None, 50]}, 'bar': {'color': "green"}}))
            st.plotly_chart(fig4, use_container_width=True, key="chart4")

            # Создаем второй индикатор шкалы (например, для влажности или другой метрики)
            last_temperature2 = all_data_sorted.iloc[0]['Brightness']
            fig_gauge2 = px.histogram(all_data, x='Temperature', title='Temperature Distribution')

            # Графики для температур
            fig_temp1 = px.line(all_data, x="EventProcessedUtcTime", y="Temperature", title="Temperature Over Time")
            fig_temp1.update_traces(line=dict(color='red'))
            fig_temp2 = px.line(all_data, x="EventProcessedUtcTime", y="Humidity", title="Humidity Over Time")
            fig_temp2.update_traces(line=dict(color='blue'))

            # Отображаем шкалы и графики
            bar_temp1.plotly_chart(fig_temp1, key=f'temperature_gauge_{i}')
            bar_temp2.plotly_chart(fig_gauge2, key=f'temperature_gauge2_{i}')

            chart_temp1.plotly_chart(fig_temp2, key=f'temperature_chart_{i}')
            chart_temp2.plotly_chart(fig_gauge1, key=f'humidity_chart_{i}')


        time.sleep(refresh_interval)

if __name__ == '__main__':
    main()
