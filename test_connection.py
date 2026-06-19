import os
import requests
import cloudinary
import cloudinary.api
from dotenv import load_dotenv

load_dotenv("config.env")

IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

ig_ok = False
cld_ok = False

# 1. Instagram test
try:
    url = f"https://graph.facebook.com/v21.0/{IG_USER_ID}"
    params = {"fields": "username", "access_token": IG_ACCESS_TOKEN}
    r = requests.get(url, params=params, timeout=30)
    data = r.json()
    if r.status_code == 200 and "username" in data:
        print(f"INSTAGRAM OK: {data['username']}")
        ig_ok = True
    else:
        print("INSTAGRAM ERROR:", data)
except Exception as e:
    print("INSTAGRAM ERROR:", e)

# 2. Cloudinary test
try:
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )
    cloudinary.api.ping()
    print("CLOUDINARY OK")
    cld_ok = True
except Exception as e:
    print("CLOUDINARY ERROR:", e)

# 3. Final
if ig_ok and cld_ok:
    print("ALL GOOD")
