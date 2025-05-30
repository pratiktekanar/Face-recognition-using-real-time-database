import firebase_admin
from firebase_admin import credentials, db
from imagekitio import ImageKit
import json

# Load ImageKit config
with open("serviceAccountKey.json", "r") as config_file:
    config = json.load(config_file)

imagekit = ImageKit(
    public_key=config["public_key"],
    private_key=config["private_key"],
    url_endpoint=config["url_endpoint"]
)


# 📤 Upload image to ImageKit
with open("Images/321654.jpg", "rb") as f:
    result = imagekit.upload(file=f, file_name="312654.jpg")

if hasattr(result, "file_id") and result.file_id:
    image_url = result.url
    print("✅ Image uploaded:", image_url)
else:
    print("❌ Upload failed.")
    image_url = None

# 🔗 Connect to Firebase
cred = credentials.Certificate("serviceAccountKeyFirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-39b75-default-rtdb.firebaseio.com/"
})

# 📦 Prepare data with ImageKit URL
ref = db.reference('Students')

data = {
    "312654": {
        "name": "Pratik Tekanar",
        "major": "AI & DS",
        "starting_year": 2021,
        "total_attendance": 6,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2024-12-11 00:54:34",
        "image_url": image_url
    },

    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)

# 📤 Send to Firebase
ref.set(data)
print("✅ Student data uploaded to Firebase.")
