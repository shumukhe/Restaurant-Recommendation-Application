import os
import cloudinary
import cloudinary.uploader
import time

# Set credentials (could use dotenv or os.environ for safety)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

photo_folder = os.path.join("static", "photos")
cloudinary_folder = "Home"

image_files = [f for f in os.listdir(photo_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for i, filename in enumerate(image_files):
    file_path = os.path.join(photo_folder, filename)
    try:
        response = cloudinary.uploader.upload(
            file_path,
            folder=cloudinary_folder,
            public_id=os.path.splitext(filename)[0],
            overwrite=True
        )
        print(f"[{i+1}/{len(image_files)}] Uploaded: {filename} ✅")
    except Exception as e:
        print(f"[{i+1}/{len(image_files)}] Failed: {filename} ❌ - {e}")
        time.sleep(1)

print("\n✅ All uploads completed!")
