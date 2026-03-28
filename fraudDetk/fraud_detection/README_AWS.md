# Deploying Fraud Detection App to AWS EC2

This guide walks you through deploying the `fraud_detection` project to an Amazon EC2 instance using Docker and Docker Compose.

## Prerequisites
1.  **An AWS Account**.
2.  **Basic AWS knowledge** (ability to launch an EC2 instance).
3.  Have this project directory on your local machine.

## Step 1: Launch an EC2 Instance
1.  Log into your AWS Management Console.
2.  Go to **EC2** and click **Launch Instance**.
3.  **Name**: `Fraud-Detection-Server`
4.  **AMI (Amazon Machine Image)**: Select **Ubuntu Server 22.04 LTS** (or 20.04).
5.  **Instance Type**: `t2.medium` or larger (Docker containers + ML models require some RAM; `t2.micro` might freeze).
6.  **Key Pair**: Create a new key pair (e.g., `fraud_app_key.pem`) and download it.
7.  **Network Settings (Security Group)**:
    *   Allow SSH traffic from anywhere.
    *   Allow HTTP traffic from anywhere.
    *   **Custom TCP Rules**: Add rules to open **Port 5000** (API) and **Port 8501** (Dashboard).
8.  Click **Launch Instance**.

## Step 2: Upload Files to EC2
You need to copy your local project folder to the EC2 instance. Use `scp` command from your local terminal (Windows PowerShell or Git Bash):

```bash
# Navigate to the parent folder of fraud_detection
cd /path/to/folder/above/project

# Copy the entire directory securely to your EC2 instance
# Replace '<your-ip>' with the Public IPv4 address of your EC2 instance
scp -i path/to/fraud_app_key.pem -r fraud_detection ubuntu@<your-ip>:/home/ubuntu/
```

## Step 3: Connect to EC2
Connect to your running EC2 instance via SSH:
```bash
ssh -i path/to/fraud_app_key.pem ubuntu@<your-ip>
```

## Step 4: Run the Deployment Script
Once logged into the EC2 instance, navigate to the folder and run the setup script:
```bash
cd fraud_detection
chmod +x deploy.sh
./deploy.sh
```

This script will:
- Update the server.
- Install Docker and Docker Compose.
- Build and spin up the API (`fraud_api`), Dashboard (`fraud_dashboard`), and MySQL Database (`fraud_db`).

## Step 5: Access the Application
- **Streamlit Dashboard**: Open your browser and go to `http://<your-ec2-ip>:8501`
- **Flask API Endpoint**: `http://<your-ec2-ip>:5000/predict`

> **Note**: To permanently use your Gmail for alerts, consider creating an App Password and keeping it out of the raw codebase. Our code is now set up to use Environment Variables (`os.getenv`), so you can securely set them in `docker-compose.yml` or via a `.env` file on the server.
