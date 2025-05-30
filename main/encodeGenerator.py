import cv2
import face_recognition
import pickle
import os
import json
from imagekitio import ImageKit

# 🔐 Load ImageKit credentials from config
with open("serviceAccountKey.json", "r") as config_file:
    config = json.load(config_file)

imagekit = ImageKit(
    public_key=config["public_key"],
    private_key=config["private_key"],
    url_endpoint=config["url_endpoint"]
)

# 📁 Import student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print("🖼️ Found images:", pathList)

imgList = []
studentIds = []
image_urls = {}  # Optional: store uploaded ImageKit URLs

for path in pathList:
    full_path = os.path.join(folderPath, path)
    img = cv2.imread(full_path)
    if img is None:
        print(f"⚠️ Skipping unreadable file: {full_path}")
        continue

    imgList.append(img)
    student_id = os.path.splitext(path)[0]
    studentIds.append(student_id)

    # 📤 Upload to ImageKit
    with open(full_path, "rb") as f:
        result = imagekit.upload(file=f, file_name=path)
        if hasattr(result, "url") and result.url:
            image_urls[student_id] = result.url
            print(f"✅ Uploaded {path} to ImageKit:", result.url)
        else:
            print(f"❌ Failed to upload {path}")

print("👤 Student IDs:", studentIds)

# 😁 Encode faces
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encodeList.append(encodings[0])
        else:
            print("⚠️ Face not found in one of the images")
            encodeList.append(None)
    return encodeList

print("✨ Encoding Started ...")
encodeListKnown = findEncodings(imgList)

# Remove None encodings and match studentIds
filtered_encodings = []
filtered_ids = []

for enc, sid in zip(encodeListKnown, studentIds):
    if enc is not None:
        filtered_encodings.append(enc)
        filtered_ids.append(sid)

encodeListKnownWithIds = [filtered_encodings, filtered_ids]
print("✅ Encoding Complete")

# 💾 Save encodings
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("💾 Encoded file saved as 'EncodeFile.p'")

# (Optional) Save image URLs
with open("ImageURLs.json", "w") as url_file:
    json.dump(image_urls, url_file, indent=4)
print("🌐 ImageKit URLs saved to 'ImageURLs.json'")
