# IoT Azure Hydroponics System

Welcome to the **IoT Azure Hydroponics System** repository! This project demonstrates an end-to-end implementation of a smart hydroponics solution, leveraging IoT devices, cloud services, and automation to monitor and manage plant growth efficiently.

---

## 📋 Project Overview
The **IoT Azure Hydroponics System** is a smart agricultural solution that integrates IoT sensors, cloud services, and real-time data processing to monitor hydroponic systems. This ensures optimized conditions for plant growth while minimizing manual intervention.

The system is designed to operate inside a **grow box**. It collects data from sensors measuring:
- **Humidity**
- **Light intensity**
- **Temperature**

The collected data is sent to **Azure IoT Hub** for analysis and storage in CSV format in **Azure Blob Storage**. The data is then visualized using the **Streamlit** library to create an interactive web-based dashboard with insightful infographics.

The system also **controls pumps, lights, and ventilation** based on sensor readings, ensuring optimal plant growth conditions.

### Key Features
- 🌱 **Real-Time Monitoring**: Tracks temperature, humidity, and light levels.
- ☁️ **Azure Integration**: Sends sensor data to Azure IoT Hub for cloud-based processing and storage.
- 📊 **Streamlit Dashboard**: Displays data as user-friendly infographics on a website.
- 🗄️ **Data Storage**: Stores data in CSV format within Azure Blob Storage.
- 🔌 **Automated Control**: Manages pumps, lights, and ventilation based on sensor readings.
- 🔍 **Future ML Integration**: Data collection to train machine learning models for advanced predictions.
- 📹 **Future Video Streaming**: Plan to integrate cameras and display live video feeds on the website.

---

## ⚙️ System Architecture
The project utilizes a modular IoT architecture with the following components:

1. **IoT Sensors and Devices**
   - Humidity Sensor
   - Temperature Sensor
   - Light Intensity Sensor

2. **Edge Processing**
   - Microcontroller (e.g., ESP32/Arduino) for sensor data collection.
   - Data sent to Azure IoT Hub via MQTT protocol.

3. **Azure Cloud Services**
   - **Azure IoT Hub**: Handles device connectivity and data ingestion.
   - **Azure Blob Storage**: Stores collected sensor data in CSV format.
   - **Streamlit**: Visualizes the data on a user-friendly web dashboard.

4. **Automated Control**
   - Controls pumps, lights, and ventilation systems based on sensor data.

5. **User Interaction**
   - Web-based dashboard for monitoring system performance and visualizing data.
   - Planned **video camera integration** for live stream visualization.

---

## 📊 Data Flow Diagram
Below is the high-level data flow of the system:

```
[ IoT Sensors ] → [ ESP32/Arduino ] → [ Azure IoT Hub ] → [ Azure Blob Storage ] → [ Streamlit Dashboard ]
                                                ↘
                                    [ Automated Control (Pumps, Lights, Ventilation) ]
```

---

## 🚀 Future Improvements
This project can be further enhanced with the following features:
- 🌐 **Machine Learning Models** to predict and optimize plant growth conditions.
- 📹 **Video Camera Integration** to monitor plants with live video streaming.

---

## 📞 Contact
For any questions, suggestions, or collaborations, feel free to contact:

**Author**: 
**Email**: 


