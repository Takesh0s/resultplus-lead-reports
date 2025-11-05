import requests, os, json
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("HELENA_API_URL")
TOKEN = os.getenv("HELENA_API_KEY")

url = f"{BASE}/chat/v1/session/search"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

body = {
    "startDate": "2025-10-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "page": 0,
    "size": 20,
    "sort": [{"property": "createdAt", "direction": "DESC"}]
}

print("🔍 Testando POST em /chat/v1/session/search ...")
r = requests.post(url, headers=headers, json=body)
print("Status:", r.status_code)
print(r.text[:1000])