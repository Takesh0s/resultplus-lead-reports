"""
find_new_endpoint.py
---------------------
Attempts to discover active or undocumented API endpoints in the Helena CRM.

This script systematically tests a list of potential endpoint paths to detect
which ones respond successfully or return data indicating valid chat sessions.

Environment variables required:
- HELENA_API_URL: Base URL of the Helena API
- HELENA_API_KEY: Bearer token for authentication
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("HELENA_API_URL", "https://api.chat.resultplus.com.br")
TOKEN = os.getenv("HELENA_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

PARAMS = {
    "startDate": "2025-10-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "size": 5
}

ENDPOINTS = [
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

print(f"🔍 Scanning potential endpoints under: {BASE_URL}\n")

for path in ENDPOINTS:
    url = f"{BASE_URL}{path}"
    try:
        print(f"➡️ Testing: {url}")
        response = requests.get(url, headers=HEADERS, params=PARAMS, timeout=15)
        status = response.status_code
        content_preview = response.text.strip()[:300]

        print(f"   → Status: {status}")
        print(f"   → Response snippet: {content_preview}")

        if any(m in content_preview for m in ["2025-10", "2025-09", "2025-11"]):
            print("✅ Possible valid endpoint (contains recent data!)")
        elif "InternalPort" in content_preview or "Incorrect URL" in content_preview:
            print("⚠️ Internal routing error (likely incorrect path)")
        elif "Not Found" in content_preview or status == 404:
            print("❌ Not found")
        elif status == 500:
            print("⚠️ Internal server error")
        else:
            print("ℹ️ Responded but no recent data")

        print("-" * 80)

    except Exception as e:
        print(f"❌ Error testing {url}: {e}")
        print("-" * 80)