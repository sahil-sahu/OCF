# 🌊 OceanTech: Real-Time Hydrodynamic Risk Monitoring System

A final-year engineering project developed around a **10-meter flume-based Open Channel Flow (OCF) setup**, OceanTech 🤖 is a smart prototype designed to assess **soil erosion, wave energy**, and **structural stress** using a combination of:

- Hydraulics + Fluid Modeling
- IoT & Edge Devices
- Machine Learning (ML)
- Distributed Systems with Apache Kafka
- Real-Time Dashboards with Grafana

---

## 📸 Project Preview
![1747559746215](https://github.com/user-attachments/assets/67cdd47b-469f-410b-bc25-d4f870f179e5)

### 🔧 Flume-Based Setup
![1747559752465](https://github.com/user-attachments/assets/b273a0d4-b2e3-40eb-adad-55d344386c99)
![1747559752267](https://github.com/user-attachments/assets/93fbe56d-ba60-4d08-81c6-e6a771474dd1)


### 📡 IoT Sensors & Data Collection
![1747559754725](https://github.com/user-attachments/assets/ab5a26c4-a50a-4d07-a1eb-35be47c1512a)
![Screenshot (12)](https://github.com/user-attachments/assets/22454f7a-ff44-40b5-92c2-4c34ea108513)


### 📊 Real-Time Grafana Dashboard
![1747559744102](https://github.com/user-attachments/assets/34124bfa-8a5d-416f-ad8e-89e60a7c1fd6)


---

## 🚀 Key Features

- **Real-Time Data Collection** using embedded sensors to monitor:
  - Flow rate
  - Wave height
  - Soil displacement
  - Vibration/strain on structures

- **Kafka-Based Streaming Pipeline** for:
  - Reliable ingestion of time-series data
  - Scaling to future deployments (bridges, embankments)

- **ML Model** for:
  - Predicting zones of maximum shear stress
  - Classifying erosion risk
  - Forecasting potential bridge collapse or landslide likelihood

- **Grafana Integration**:
  - Interactive dashboards
  - Real-time visualization of system health and environment parameters

- **Localhost + Edge Device Server**:
  - Offline-first design with fallback to central cloud
  - Raspberry Pi or equivalent for edge processing

---

## 🧠 Architecture Overview

```mermaid
graph TD
  A[IoT Sensors - ESP32] --> B[MQTT Broker]
  B --> C[MQTT-Kafka Connect]
  C --> D[Kafka Broker]
  D --> E[Kafka Consumer - Wave Processor]
  E --> F[ML Model - Prediction Engine]
  E --> G[InfluxDB - Time Series Storage]
  E --> H[S3 - Long Term Storage]
  G --> I[Grafana Dashboard]

