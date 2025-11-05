import requests, os, itertools, time
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("HELENA_API_URL", "https://api.chat.resultplus.com.br")
URL = f"{BASE}/chat/v1/session"
TOKEN = os.getenv("HELENA_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json,text/plain,*/*",
    "User-Agent": "param-discovery/1.0"
}

date_samples = [
    ("startDate", "2025-10-01T00:00:00Z"),
    ("endDate", "2025-10-31T23:59:59Z"),
    ("fromDate", "2025-10-01"),
    ("toDate", "2025-10-31"),
    ("after", "2025-09-30T00:00:00Z"),
    ("since", "2025-10-01T00:00:00Z"),
]
paging = [
    ("page", "0"), ("page", "1"), ("page", "2"),
    ("size", "10"), ("size", "20"), ("size", "50"), ("size", "100"),
    ("limit", "20"), ("limit", "50"), ("offset", "0"), ("offset", "50"),
    ("skip", "0"), ("skip", "50")
]
sorts = [
    ("sort", "createdAt,desc"),
    ("sort", "createdAt:desc"),
    ("order", "desc"),
    ("orderBy", "createdAt"),
]

combos = []
for d in date_samples:
    for p in paging:
        combos.append({d[0]: d[1], p[0]: p[1]})
    combos.append({d[0]: d[1]})

extended = []
for c in combos:
    extended.append(c)
    for s in sorts:
        new = dict(c)
        new[s[0]] = s[1]
        extended.append(new)
combos = extended

extra_pairs = [
    {"page": "0", "size": "50"},
    {"page": "1", "size": "50"},
    {"page": "2", "size": "50"},
    {"limit": "100", "offset": "0"},
]
combos.extend(extra_pairs)

seen = set()
unique_combos = []
for c in combos:
    k = tuple(sorted(c.items()))
    if k not in seen:
        seen.add(k)
        unique_combos.append(c)

print(f"🔍 Testando {len(unique_combos)} combinações em: {URL}\n(tempo estimado: ~{len(unique_combos)*0.4:.1f}s)")

found_any = False
for i, params in enumerate(unique_combos, 1):
    try:
        r = requests.get(URL, headers=HEADERS, params=params, timeout=12)
        status = r.status_code
        text = r.text[:2000]
        if "2025-10" in text or "2025-11" in text:
            print(f"\n✅ POSSÍVEL ACERTO na combinação #{i} -> status {status}")
            print("params =", params)
            print("trecho resposta:\n", text[:1200])
            found_any = True
            break
        else:
            if i % 10 == 0 or status not in (200, 404, 500):
                print(f"[{i}/{len(unique_combos)}] status {status} params={params} (sem datas recentes)")
    except Exception as e:
        print(f"[{i}] Erro com params={params} -> {e}")
    time.sleep(0.25)

if not found_any:
    print("\n❌ Não encontramos respostas com datas de out/nov usando esses parâmetros comuns.")
    print("Próximos passos recomendados:")
    print(" - testar com sessão autenticada (cookie) do painel,")
    print(" - contatar suporte ResultPlus para endpoint/datas,")
    print(" - ou solicitar o swagger.json interno.")
else:
    print("\n🎯 Achou — pare o script e me mande o bloco de saída acima.")