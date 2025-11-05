"""
Module: scan_swagger
--------------------

Performs an automated scan of potential Swagger and OpenAPI endpoints
for a specified base domain. The script attempts to discover public or
semi-public documentation endpoints such as `/swagger.json`, `/openapi.json`,
or Swagger UI interfaces.

This utility assists in identifying whether an API exposes its schema
or documentation in a predictable location, often useful for diagnostics
and integration validation tasks.
"""

import requests


BASE_URL = "https://chat.resultplus.com.br"

# Common Swagger and OpenAPI documentation paths
PATHS = [
    "/swagger",
    "/swagger/",
    "/swagger/index.html",
    "/swagger/v1/swagger.json",
    "/swagger/v2/swagger.json",
    "/swagger/v3/swagger.json",
    "/chat/swagger",
    "/chat/v1/swagger.json",
    "/chat/v2/swagger.json",
    "/chat/v3/swagger.json",
    "/chat2/swagger.json",
    "/chat2/v1/swagger.json",
    "/chat2/v2/swagger.json",
    "/api/swagger.json",
    "/api/v1/swagger.json",
    "/openapi.json",
    "/openapi/v1.json",
    "/docs",
    "/api-docs",
    "/v1/api-docs",
    "/swagger-resources",
    "/swagger-resources/configuration/ui",
    "/swagger-resources/configuration/security",
]


def scan_swagger_endpoints():
    """
    Scans the predefined paths under the base domain and reports the HTTP
    response status, content type, and any indications of Swagger/OpenAPI
    documentation or UI pages.

    This function prints formatted diagnostic messages to the console.
    """
    print(f"🔍 Scanning Swagger/OpenAPI endpoints for domain: {BASE_URL}\n")

    for path in PATHS:
        url = BASE_URL + path
        try:
            response = requests.get(url, timeout=5)
            code = response.status_code
            content_type = response.headers.get("Content-Type", "")

            if code == 200 and ("json" in content_type or "html" in content_type):
                print(f"✅ {url} → {code} ({content_type})")
                if "json" in content_type:
                    print("📄 Snippet:", response.text[:300], "\n")
                else:
                    print("🌐 HTML page detected (possibly Swagger UI)\n")
            elif code in (401, 403):
                print(f"🔒 {url} → {code} (restricted access)")
            elif code == 404:
                # Common case — endpoint does not exist
                continue
            else:
                print(f"⚠️ {url} → {code}")
        except requests.exceptions.RequestException as error:
            print(f"❌ Error accessing {url}: {error}")

    print("\n🧭 Scan completed!")


if __name__ == "__main__":
    scan_swagger_endpoints()