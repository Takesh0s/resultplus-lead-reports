import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = f"{os.getenv('HELENA_API_URL')}/chat/v1/session"
TOKEN = os.getenv("HELENA_API_KEY")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("🔍 Testando paginação na API Helena...\n")

for page in range(0, 5):
    params = {"page": page, "size": 50}
    try:
        r = requests.get(API_URL, headers=headers, params=params, timeout=15)
        print(f"📄 Página {page} | Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            items = data.get("items") or []
            if items:
                first = items[0].get("createdAt")
                last = items[-1].get("createdAt")
                print(f" - Itens: {len(items)} | De {first} até {last}")
            else:
                print(" - Nenhum item nesta página.")
        else:
            print(" - Resposta:", r.text[:300])
    except Exception as e:
        print("❌ Erro:", e)
    print("-" * 80)