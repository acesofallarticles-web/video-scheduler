import os
import sys
import time

import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

GRAPH = "https://graph.facebook.com/v21.0"

# ---- CONFIG ----
load_dotenv("config.env")

IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def main():
    # ---- ARGS ----
    if len(sys.argv) < 3:
        print('Usage: python post_one.py "lesson1.mp4" "My caption here"')
        sys.exit(1)

    filename = sys.argv[1]
    caption = sys.argv[2]
    video_path = os.path.join("videos", filename)

    # ---- STEP 1: check file ----
    print(f"[1/5] Checking video file: {video_path}")
    if not os.path.isfile(video_path):
        print(f"ERROR: file not found -> {video_path}")
        sys.exit(1)
    print("      File found.")

    # ---- STEP 2: upload to Cloudinary ----
    print("[2/5] Uploading video to Cloudinary (this can take a while)...")
    try:
        result = cloudinary.uploader.upload_large(
            video_path, resource_type="video"
        )
        secure_url = result["secure_url"]
    except Exception as e:
        print(f"ERROR: Cloudinary upload failed -> {e}")
        sys.exit(1)
    print(f"Uploaded to Cloudinary: {secure_url}")

    # ---- STEP 3: create media container ----
    print("[3/5] Creating Instagram media container...")
    try:
        r = requests.post(
            f"{GRAPH}/{IG_USER_ID}/media",
            params={
                "media_type": "REELS",
                "video_url": secure_url,
                "caption": caption,
                "access_token": IG_ACCESS_TOKEN,
            },
            timeout=60,
        )
        data = r.json()
    except Exception as e:
        print(f"ERROR: container request failed -> {e}")
        print("Response text:", getattr(r, "text", "<no response>"))
        sys.exit(1)

    if r.status_code != 200 or "id" not in data:
        print("ERROR creating container. Full response:")
        print(data)
        sys.exit(1)

    container_id = data["id"]
    print(f"Container created: {container_id}")

    # ---- STEP 4: poll container status ----
    print("[4/5] Waiting for Instagram to process the video...")
    max_attempts = 60
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.get(
                f"{GRAPH}/{container_id}",
                params={
                    "fields": "status_code",
                    "access_token": IG_ACCESS_TOKEN,
                },
                timeout=60,
            )
            status = r.json()
        except Exception as e:
            print(f"      WARN: status check failed -> {e}; retrying...")
            time.sleep(5)
            continue

        status_code = status.get("status_code")
        print(f"      [{attempt}/{max_attempts}] Status: {status_code}")

        if status_code == "FINISHED":
            break
        if status_code == "ERROR":
            print("ERROR: container processing failed. Full response:")
            print(status)
            sys.exit(1)

        time.sleep(5)
    else:
        print("ERROR: timed out waiting for container to finish (5 min).")
        sys.exit(1)

    # ---- STEP 5: publish ----
    print("[5/5] Publishing the Reel...")
    try:
        r = requests.post(
            f"{GRAPH}/{IG_USER_ID}/media_publish",
            params={
                "creation_id": container_id,
                "access_token": IG_ACCESS_TOKEN,
            },
            timeout=60,
        )
        data = r.json()
    except Exception as e:
        print(f"ERROR: publish request failed -> {e}")
        print("Response text:", getattr(r, "text", "<no response>"))
        sys.exit(1)

    if r.status_code != 200 or "id" not in data:
        print("ERROR publishing. Full response:")
        print(data)
        sys.exit(1)

    print(f"PUBLISHED! Media ID: {data['id']}")


if __name__ == "__main__":
    main()
