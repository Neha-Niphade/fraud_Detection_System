from flask import Flask, request, jsonify
import joblib
import numpy as np
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import os
# Function to send email alert
def send_alert():
    print("🚨 Sending email alert...")
    sender = os.getenv("EMAIL_SENDER", "kabadeketan2@gmail.com")
    receiver = os.getenv("EMAIL_RECEIVER", "amanpokale06@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "zgzwgbknttreozgu")

    msg = MIMEText("Fraudulent transaction detected!")
    msg["Subject"] = "Fraud Alert"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
#database connection    
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "kk02"),
    database=os.getenv("DB_NAME", "fraud_db")
)

cursor = db.cursor()

print("Running app.py...")
app = Flask(__name__)

# Load model
try:
    model = joblib.load("fraud_model.pkl")
    print("Model loaded successfully")
except Exception as e:
    print("Error loading model:", e)

@app.route('/')
def home():
    return "Fraud Detection API is running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Convert input into array
    features = np.array(data['features']).reshape(1, -1)
    #prediction
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]
    result = "Fraud" if prediction == 1 else "Not Fraud"
    if result == "Fraud":
        send_alert()
    cursor.execute(
    "INSERT INTO transactions (features, prediction) VALUES (%s, %s)",
    (str(data['features']), result)
    )
    print("Saving to DB...")
    
    db.commit()
    print("Saved successfully")

    return jsonify({
    "prediction": result,
    "probability": float(prob)
})

if __name__ == '__main__':
    app.run(debug=False)