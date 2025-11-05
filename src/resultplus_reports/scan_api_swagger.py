"""
scan_api_swagger.py
~~~~~~~~~~~~~~~~~~~

Script to scan a target API for public Swagger/OpenAPI endpoints.

This tool attempts to locate common Swagger and OpenAPI JSON definition
files within a given API base URL. It helps developers identify
documentation endpoints for testing, integration, or security analysis.

Example:
    $ python scan_api_swagger.py

Environment:
    The BASE constant should be set to the target API root URL.
"""

import requests
from urllib.parse import urljoin


# Base API endpoint to scan
BASE = "https://api.chat.resultplus.com.br"

# Standard request headers for scanning
HEADERS = {
    "Accept": "application/json, text/html, */*",
    "User-Agent": "scan-swagger-script/1.0"
}

# Common Swagger and OpenAPI endpoint paths
PATHS = [
    "/swagger/v1/swagger.json",
    "/swagger/v2/swagger.json",
    "/swagger.json",
    "/openapi.json",
    "/openapi/v1.json",
    "/api-docs",
    "/v1/api-docs",
    "/swagger-resources",
    "/swagger-resources/configuration/ui",
    "/swagger-resources/configuration/security",
    "/doc/swagger.json",
    "/docs/swagger.json",
    "/api/swagger.json",
    "/api/v1/swagger.json",
    "/api/openapi.json",
    "/.well-known/openapi.json",
]


def scan_swagger_endpoints(base_url: str = BASE) -> None:
    """
    Scans the target API for Swagger/OpenAPI endpoints.

    Args:
        base_url (str): The root URL of the target API.

    Behavior:
        Prints the result of each attempted request, including status codes,
        content type, and the first portion of the response body when relevant.
    """
    print(f"🔍 Scanning {base_url} for Swagger/OpenAPI JSON endpoints...\n")

    for path in PATHS:
        url = urljoin(base_url, path)
        try:
            response = requests.get(
                url, headers=HEADERS, timeout=10, allow_redirects=True
            )

            code = response.status_code
            content_type = response.headers.get("Content-Type", "")

            print(f"➡️ {url}  → {code}  ({content_type})")

            if code == 200 and "json" in content_type:
                snippet = response.text[:1000]
                print("✅ JSON found! Preview:\n")
                print(snippet)
                print("\n---\n")

            elif code == 200 and "html" in content_type:
                snippet = response.text[:800]
                print("ℹ️ HTML returned (possible Swagger UI). Preview:\n")
                print(snippet)
                print("\n---\n")

            elif code in (401, 403):
                print("🔒 Restricted access (401/403). Authentication may be required.\n---\n")

            elif code in (404, 405):
                print("⛔ Not found or method not allowed.\n---\n")

            else:
                print("ℹ️ Unexpected response. Preview:\n")
                print(response.text[:400])
                print("\n---\n")

        except requests.exceptions.RequestException as e:
            print(f"❌ Request error while accessing {url}: {e}\n---\n")

    print("🧭 Scan completed.")


if __name__ == "__main__":
    scan_swagger_endpoints()