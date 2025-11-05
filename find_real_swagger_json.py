import requests
import re

BASE = "https://chat.resultplus.com.br/swagger/"

print(f"🔍 Buscando arquivo JSON real em {BASE}\n")

try:
    html = requests.get(BASE, timeout=10).text
    
    matches = re.findall(r'swaggerUrl\s*:\s*"([^"]+)"', html)
    if not matches:
        matches = re.findall(r'url\s*:\s*"([^"]+)"', html)

    if matches:
        print("✅ Swagger JSON encontrado:")
        for m in matches:
            print("-", m)
    else:
        print("⚠️ Nenhum swaggerUrl/url encontrado no HTML.")
        print("Verifique se o conteúdo está ofuscado ou carregado por script remoto.")

        alt = "https://chat.resultplus.com.br/swagger-resources"
        r2 = requests.get(alt, timeout=10)
        if r2.status_code == 200:
            print(f"\n📡 /swagger-resources retornou {len(r2.text)} caracteres:\n")
            print(r2.text[:500])
        else:
            print(f"❌ /swagger-resources retornou código {r2.status_code}")

except Exception as e:
    print("❌ Erro:", e)