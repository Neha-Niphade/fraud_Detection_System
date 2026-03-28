# 🛡️ Fraud Sentinel AI

**Fraud Sentinel** is a real-time, end-to-end Machine Learning web application designed to detect fraudulent transactions instantly. 

Built with a **Flask API** backend for serving predictions, a sleek **Streamlit** frontend for real-time monitoring and analytics, and a **MySQL** database for secure log storage. The entire infrastructure is cleanly containerized using **Docker** and perfectly configured for cloud deployment on **AWS EC2**.

![Dashboard Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![AWS](https://img.shields.io/badge/AWS-EC2_Deployed-orange)

---

## Key Features
*  **Machine Learning Engine**: High-speed, highly-accurate fraud classification using `scikit-learn`.
**Real-Time Analytics Dashboard**: Glassmorphism UI built with Streamlit and Plotly for deep visual insights and metrics.
 **Automated Alert System**: Instantly triggers email alerts via `smtplib` the moment a fraudulent transaction is detected.
**Persistent Database**: Automatically logs all transaction attempts (Fraud vs Secure) to a MySQL database.
**Containerized Infrastructure**: Fully orchestrated with Docker Compose for seamless "`one-click`" deployment.

---

## Technology Stack
* **Frontend**: Streamlit, Plotly, Pandas
* **Backend**: Python, Flask, Joblib
* **Machine Learning**: Scikit-Learn, NumPy
* **Database**: MySQL 8.0
* **DevOps / Deployment**: Docker, Docker Compose, Bash, AWS EC2, Ubuntu 24.04

---

## Running Locally (Using Docker)
You don't need to manually install dependencies or set up a local database. Docker handles everything!

### Prerequisites:
* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Quick Start:
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/fraud-sentinel.git
   cd fraud-sentinel
   ```
2. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up -d --build
   ```
3. Open your browser and go to:
   * **Dashboard**: `http://localhost:8501`
   * **API Status**: `http://localhost:5000`

---

##  Deploying to AWS EC2

This project includes a custom `deploy.sh` script specifically designed to set up the entire environment on a fresh AWS Ubuntu server automatically!

### 1. Launch & Connect
* Launch an **Ubuntu Server 22.04 / 24.04** on AWS (a `t3.micro` or larger is recommended).
* **Important**: Make sure to allocate a minimum of **15GB-20GB** of EBS storage, as the Machine Learning libraries require space to build.
* In your AWS Security Groups, open Inbound **Port 8501** (Dashboard) and **Port 5000** (API) to `0.0.0.0/0`.
* Connect to your server via SSH.

### 2. Copy the Project
From your local computer, use `scp` to securely copy this project to your new server (Make sure to exclude your `.venv` folder!):
```bash
scp -i "your-key.pem" -r fraud-sentinel ubuntu@<your-ec2-ip>:/home/ubuntu/
```

### 3. Run the Automated Deployment
SSH into your server and run the script:
```bash
cd fraud-sentinel
chmod +x deploy.sh
./deploy.sh
```
*The script automatically installs Docker, configures virtual Memory (Swap) for low-RAM instances, and builds the database, API, and frontend concurrently.*

### 4. Live!
Once finished, your app is globally accessible at:
👉 `http://<your-ec2-ip>:8501`

---

## Project Structure
```text
fraud_detection/
├── app.py                  # Flask API & Email Alert Logic
├── dashboard.py            # Streamlit Frontend & Analytics
├── fraud_model.pkl         # Serialized Scikit-Learn Model
├── init.sql                # MySQL Table Initialization
├── requirements.txt        # Python Dependencies
├── api.Dockerfile          # Docker instructions for the Backend
├── dashboard.Dockerfile    # Docker instructions for the Frontend
├── docker-compose.yml      # Service Orchestration (App, UI, DB)
└── deploy.sh               # AWS Ubuntu Deployment Script
```

---

