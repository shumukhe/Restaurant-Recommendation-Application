import os
import cloudinary
import cloudinary.uploader
import time

# Set credentials (could use dotenv or os.environ for safety)
cloudinary.config(
    cloud_name="dnsvyb8zc",
    api_key="554669476784921",
    api_secret="Lk2uz4LVDLOK9KE4xDLEW4AEJU0"
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
