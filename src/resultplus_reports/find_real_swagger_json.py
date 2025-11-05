"""
find_real_swagger_json.py
--------------------------
Attempts to locate the real Swagger JSON file for the Helena CRM API.

This script scans the public Swagger UI page to detect embedded JSON references,
and falls back to checking `/swagger-resources` if not directly visible.

Usage:
    python find_real_swagger_json.py
"""

import re
import requests

BASE_URL = "https://chat.resultplus.com.br/swagger/"

print(f"🔍 Searching for Swagger JSON definitions at {BASE_URL}\n")

try:
    html = requests.get(BASE_URL, timeout=10).text
    matches = re.findall(r'swaggerUrl\s*:\s*"([^"]+)"', html)

    if not matches:
        matches = re.findall(r'url\s*:\s*"([^"]+)"', html)

    if matches:
        print("✅ Swagger JSON reference(s) found:")
        for m in matches:
            print(f"   → {m}")
    else:
        print("⚠️ No swaggerUrl/url found in HTML.")
        print("   The Swagger UI might load content dynamically via remote script.")

        alt_url = "https://chat.resultplus.com.br/swagger-resources"
        r2 = requests.get(alt_url, timeout=10)
        if r2.status_code == 200:
            print(f"\n📡 /swagger-resources returned {len(r2.text)} characters:\n")
            print(r2.text[:500])
        else:
            print(f"❌ /swagger-resources returned HTTP {r2.status_code}")

except Exception as e:
    print(f"❌ Error fetching Swagger info: {e}")