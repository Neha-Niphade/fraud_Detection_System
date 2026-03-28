#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment setup on EC2 (Ubuntu)..."

# 1. Update system
echo "Updating packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# 1.5 Create Swap file to prevent Out-Of-Memory errors on Free Tier instances (1GB RAM)
# 1.5 Create Swap file to prevent Out-Of-Memory errors on Free Tier instances (1GB RAM)
echo "Setting up a 2GB swap file..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
else
    echo "Swapfile already exists, skipping creation to avoid errors."
fi

# 2. Install Docker
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add current user to docker group to run docker without sudo
sudo usermod -aG docker ubuntu

# 3. Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Starting the application
echo "Starting Application via Docker Compose..."
# Assuming you have copied your code to this EC2 instance into /home/ubuntu/fraud_detection
cd /home/ubuntu/fraud_detection || echo "Make sure to copy your code to /home/ubuntu/fraud_detection"
sudo /usr/local/bin/docker-compose up -d --build

echo "Deployment complete! API running on port 5000, Dashboard on port 8501."
