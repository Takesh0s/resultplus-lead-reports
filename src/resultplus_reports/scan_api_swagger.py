import requests
from urllib.parse import urljoin

BASE = "https://api.chat.resultplus.com.br"
HEADERS = {
    "Accept": "application/json, text/html, */*",
    "User-Agent": "scan-swagger-script/1.0"
}

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

print(f"🔍 Scanning {BASE} for Swagger/OpenAPI JSON endpoints...\n")

for p in PATHS:
    url = urljoin(BASE, p)
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        code = r.status_code
        ct = r.headers.get("Content-Type", "")
        print(f"➡️ {url}  → {code}  ({ct})")

        if code == 200 and "json" in ct:
            snippet = r.text[:1000]
            print("✅ JSON encontrado! Trecho inicial:\n")
            print(snippet)
            print("\n---\n")
        elif code == 200 and "html" in ct:
            snippet = r.text[:800]
            print("ℹ️ HTML retornado (possível Swagger UI). Trecho inicial:\n")
            print(snippet)
            print("\n---\n")
        elif code in (401, 403):
            print("🔒 Acesso restrito (401/403). Pode exigir autenticação.\n---\n")
        elif code in (404, 405):
            print("⛔ Não encontrado ou método não permitido.\n---\n")
        else:
            print("ℹ️ Resposta diferente. Trecho:\n")
            print(r.text[:400])
            print("\n---\n")

    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}\n---\n")

print("🧭 Scan concluído.")