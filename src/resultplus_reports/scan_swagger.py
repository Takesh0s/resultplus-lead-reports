import requests

BASE_URL = "https://chat.resultplus.com.br"

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

print("🔍 Testando endpoints Swagger/OpenAPI no domínio:", BASE_URL, "\n")

for path in PATHS:
    url = BASE_URL + path
    try:
        r = requests.get(url, timeout=5)
        code = r.status_code
        ct = r.headers.get("Content-Type", "")
        if code == 200 and ("json" in ct or "html" in ct):
            print(f"✅ {url} → {code} ({ct})")
            if "json" in ct:
                print("📄 Trecho inicial:", r.text[:300], "\n")
            else:
                print("🌐 Página HTML detectada (Swagger UI?)\n")
        elif code in (401, 403):
            print(f"🔒 {url} → {code} (acesso restrito)")
        elif code == 404:
            pass
        else:
            print(f"⚠️ {url} → {code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro em {url}: {e}")

print("\n🧭 Teste concluído!")