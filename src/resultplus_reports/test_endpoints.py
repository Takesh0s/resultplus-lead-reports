import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("HELENA_API_URL")
TOKEN = os.getenv("HELENA_API_KEY")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

endpoints = [
    f"{BASE}/chat2/session",
    f"{BASE}/chat2/v1/session",
    f"{BASE}/chat2/v1/session/search",
    f"{BASE}/chat/v2/session",
    f"{BASE}/chat/v2/session/search",
    f"{BASE}/chat/v1/session/search"
]

params = {
    "startDate": "2025-10-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "size": 5
}

print(f"🔍 Testando endpoints no domínio: {BASE}\n")

for url in endpoints:
    print(f"➡️ Testando: {url}")
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        print("Status:", r.status_code)
        
        print(r.text[:600])
        print("-" * 80)

    except Exception as e:
        print("❌ Erro:", e)
        print("-" * 80)