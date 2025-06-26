import os

# Check if model is already trained
if not os.path.exists('ml_model/cost_predictor.pkl'):
    from ml_model import train_model  # This will run the code in train_model.py

    
import paho.mqtt.client as mqtt
import firebase_admin
from firebase_admin import credentials, db
import json
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://final-project-714ab-default-rtdb.firebaseio.com/'
})

firebase_ref = db.reference('/iot_energy_logs')

# MQTT Callback
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code " + str(rc))
    client.subscribe("smartmeter/data")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        firebase_ref.push(payload)
        print("✅ Data pushed to Firebase:", payload)
    except Exception as e:
        print("❌ Error:", e)

# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Replace with your MacBook’s IP if ESP is using it
client.connect("localhost", 1883, 60)

# Start the loop
print("🔄 Listening for MQTT messages...")
client.loop_forever()