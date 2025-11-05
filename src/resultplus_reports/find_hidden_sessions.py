"""
find_hidden_sessions.py
---------------------------------
Utility script to probe possible hidden session endpoints
from the Helena CRM API, in order to identify accessible
routes under /chat/v1/session/*.

Author: [Seu Nome ou equipe]
Created: 2025-11-05
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

BASE = os.getenv("HELENA_API_URL")
TOKEN = os.getenv("HELENA_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

ROUTES = [
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

BODY = {
    "startDate": "2025-10-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "size": 5
}


def probe_sessions():
    results = []
    logging.info(f"Probing possible session endpoints under {BASE}/chat/v1/ ...")

    for route in ROUTES:
        for method in ["GET", "POST"]:
            url = f"{BASE}/chat/v1/{route}"
            try:
                response = (
                    requests.get(url, headers=HEADERS, params=BODY, timeout=10)
                    if method == "GET"
                    else requests.post(url, headers=HEADERS, json=BODY, timeout=10)
                )

                if response.status_code in [200, 400]:
                    logging.info(f"✅ {method} {url} | Status {response.status_code}")
                    results.append({
                        "method": method,
                        "url": url,
                        "status": response.status_code,
                        "response_snippet": response.text[:300]
                    })
                else:
                    logging.warning(f"❌ {method} {url} | Status {response.status_code}")

            except Exception as e:
                logging.error(f"⚠️ Error at {url}: {e}")

    return results


if __name__ == "__main__":
    found = probe_sessions()

    if found:
        out_path = f"hidden_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(found, f, indent=2, ensure_ascii=False)
        logging.info(f"Results saved to {out_path}")
    else:
        logging.info("No valid session endpoints found.")