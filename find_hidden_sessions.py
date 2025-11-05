import requests, os, json
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("HELENA_API_URL")
TOKEN = os.getenv("HELENA_API_KEY")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

routes = [
    "session",
    "session/search",
    "session/filter",
    "session/query",
    "session/find",
    "session/list",
    "session/paginate",
    "session/recent",
    "session/history",
    "session/report",
    "session/data",
    "session/export"
]

body = {
    "startDate": "2025-10-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "size": 5
}

print(f"🔍 Procurando endpoints válidos em {BASE}/chat/v1/ ...\n")

for route in routes:
    for method in ["get", "post"]:
        url = f"{BASE}/chat/v1/{route}"
        try:
            if method == "get":
                r = requests.get(url, headers=headers, params=body, timeout=10)
            else:
                r = requests.post(url, headers=headers, json=body, timeout=10)

            if r.status_code in [200, 400]:
                print(f"✅ {method.upper()} {url} | Status {r.status_code}")
                print("Resposta parcial:", r.text[:300], "\n---")
            else:
                print(f"❌ {method.upper()} {url} | Status {r.status_code}")
        except Exception as e:
            print(f"⚠️  Erro em {route}: {e}")