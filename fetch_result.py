import os
import json
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import time

load_dotenv()

BASE_URL = os.getenv("HELENA_API_URL", "https://api.chat.resultplus.com.br")
API_URL = f"{BASE_URL}/chat/v1/session"
TOKEN = os.getenv("HELENA_API_KEY")

def fetch_helena_sessions():
    print("🔄 Buscando sessões recentes do Helena CRM...")

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    params = {
        "startDate": "2025-10-01T00:00:00Z",
        "endDate": "2025-11-03T23:59:59Z",
        "sort": "createdAt,desc",
    }

    all_sessions = []
    page = 0
    last_batch_ids = set()

    while True:
        params["page"] = str(page)
        response = requests.get(API_URL, headers=headers, params=params)
        print(f"📄 Página {page} | Status: {response.status_code}")

        if response.status_code != 200:
            print("❌ Erro de resposta:", response.text[:300])
            break

        data = response.json()
        items = data.get("items", [])

        if not items:
            print("⚠️ Nenhum item retornado — fim da paginação.")
            break

        current_ids = {s.get("id") for s in items if s.get("id")}
        if current_ids == last_batch_ids:
            print("⚠️ Resultados repetidos detectados — encerrando paginação.")
            break

        last_batch_ids = current_ids
        all_sessions.extend(items)

        first = items[0].get("createdAt")
        last = items[-1].get("createdAt")
        print(f"   → {len(items)} itens (de {first} até {last})")

        page += 1
        time.sleep(0.3)

    if not all_sessions:
        print("⚠️ Nenhuma sessão encontrada.")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    leads = []
    for s in all_sessions:
        created = s.get("createdAt")
        if not created:
            continue
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt < cutoff:
            continue

        leads.append({
            "id": s.get("id"),
            "criado_em": created,
            "status": s.get("status"),
            "ultima_mensagem": s.get("lastMessageText"),
            "link_chat": s.get("previewUrl"),
        })

    if not leads:
        print("⚠️ Nenhum lead recente (últimos 7 dias).")
        return []

    with open("leads.json", "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(leads)} leads salvos em leads.json")
    return leads


if __name__ == "__main__":
    fetch_helena_sessions()