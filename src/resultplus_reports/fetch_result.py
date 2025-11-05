"""
fetch_result.py
----------------
Fetches recent chat sessions (leads) from the Helena CRM private API.

This module connects to the CRM endpoint, handles pagination automatically,
filters recent sessions (last 7 days), and exports validated data to `leads.json`.

Environment variables required:
- HELENA_API_URL: Base URL of the Helena API
- HELENA_API_KEY: Bearer token for authentication
"""

import os
import json
import time
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load .env variables (Helena API credentials, etc.)
load_dotenv()

BASE_URL = os.getenv("HELENA_API_URL", "https://api.chat.resultplus.com.br")
API_URL = f"{BASE_URL}/chat/v1/session"
TOKEN = os.getenv("HELENA_API_KEY")


def fetch_helena_sessions():
    """
    Fetch recent sessions from Helena CRM and store them in a local JSON file.

    This function handles pagination, filters sessions from the last 7 days,
    and exports structured lead data to `leads.json`.

    Returns:
        dict: Summary with total leads and output file name
    """
    print("🔄 Fetching recent sessions from Helena CRM...")

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    # --- Dynamic date range (last 30 days) ---
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)

    params = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "sort": "createdAt,desc",
    }

    all_sessions = []
    page = 0
    last_batch_ids = set()

    # --- Pagination loop ---
    while True:
        params["page"] = str(page)
        response = requests.get(API_URL, headers=headers, params=params)
        print(f"📄 Page {page} | Status: {response.status_code}")

        if response.status_code != 200:
            print("❌ Response error:", response.text[:300])
            break

        data = response.json()
        items = data.get("items", [])

        if not items:
            print("⚠️ No items returned — pagination ended.")
            break

        # Prevent infinite loop if identical results repeat
        current_ids = {s.get("id") for s in items if s.get("id")}
        if current_ids == last_batch_ids:
            print("⚠️ Duplicate batch detected — stopping pagination.")
            break

        last_batch_ids = current_ids
        all_sessions.extend(items)

        first = items[0].get("createdAt")
        last = items[-1].get("createdAt")
        print(f"   → {len(items)} items (from {first} to {last})")

        page += 1
        time.sleep(0.3)

    if not all_sessions:
        print("⚠️ No sessions found.")
        return {"count": 0, "file": None}

    # --- Filter sessions created within the last 7 days ---
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
        print("⚠️ No recent leads (last 7 days).")
        return {"count": 0, "file": None}

    # --- Save to timestamped JSON file ---
    file_name = f"leads_{datetime.now():%Y%m%d}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(leads)} leads saved to {file_name}")
    return {"count": len(leads), "file": file_name}


if __name__ == "__main__":
    result = fetch_helena_sessions()
    print(f"\n📊 Summary → {result['count']} leads exported to {result['file']}")