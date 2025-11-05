import requests, os, json
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("HELENA_API_URL")
TOKEN = os.getenv("HELENA_API_KEY")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

params = {
    "startDate": "2025-10-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "size": 5
}

paths = [
    "/chat2/session",
    "/chat2/v1/session",
    "/chat2/v1/session/search",
    "/chat2/v2/session",
    "/chat2/v2/session/search",
    "/chat/v1/session",
    "/chat/v1/session/search",
    "/chat/v2/session",
    "/chat/v2/session/search",
    "/chat/report/session",
    "/chat/v1/report",
    "/chat/v1/report/search",
    "/chat2/report/session",
    "/report/session",
    "/session",
    "/session/search",
]

print(f"🔍 Buscando endpoints ativos no domínio: {BASE}\n")

for path in paths:
    url = f"{BASE}{path}"
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        print(f"➡️ Testando: {url}")
        print("Status:", r.status_code)

        content = r.text.strip()[:300]
        print(content)

        if any(mes in content for mes in ["2025-10", "2025-09", "2025-11"]):
            print("✅ POSSÍVEL ENDPOINT CORRETO (contém dados recentes!)")
        elif "InternalPort" in content or "Incorrect URL" in content:
            print("⚠️ Caminho interno incorreto (erro de roteamento)")
        elif "Not Found" in content or r.status_code == 404:
            print("❌ Não encontrado")
        elif r.status_code == 500:
            print("⚠️ Erro interno do servidor")
        else:
            print("ℹ️ Endpoint respondeu, mas sem dados recentes")

        print("-" * 80)

    except Exception as e:
        print(f"❌ Erro ao testar {url}: {e}")
        print("-" * 80)