import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

# Load your Firebase credentials (make sure path is correct)
cred = credentials.Certificate("serviceAccountKey.json")

# Your Firebase Realtime Database URL
firebase_url = "https://final-project-714ab-default-rtdb.firebaseio.com/"

# Initialize the Firebase app (only once)
firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_url
})

# Get a reference to your desired node in the database
ref = db.reference('/iot_energy_logs')

# Sample data
data = {
    'Vrms': 230,
    'Irms': 0.42,
    'Power': 96.6,
    'kWh': 1.57,
    'Cost': 21.45,
    'Timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Push the data
ref.push(data)

print("✅ Data pushed to Firebase successfully!")