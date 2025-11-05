import os
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = "gcp-key.json"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
DOC_ID = os.getenv("DOC_ID")

def load_new_leads():
    if not os.path.exists("leads.json"):
        print("⚠️ Nenhum leads.json encontrado.")
        return []

    with open("leads.json", "r", encoding="utf-8") as f:
        leads = json.load(f)

    sent_ids = set()
    if os.path.exists("sent.json"):
        with open("sent.json", "r", encoding="utf-8") as f:
            try:
                sent_ids = set(json.load(f))
            except json.JSONDecodeError:
                sent_ids = set()

    new_leads = [l for l in leads if l["id"] not in sent_ids]

    sent_ids.update([l["id"] for l in new_leads])
    with open("sent.json", "w", encoding="utf-8") as f:
        json.dump(list(sent_ids), f, ensure_ascii=False, indent=2)

    return new_leads

def group_by_hour(leads):
    grouped = {}
    for lead in leads:
        try:
            dt = datetime.fromisoformat(lead["criado_em"].replace("Z", "+00:00"))
            hour = dt.astimezone().strftime("%H:00")
            grouped[hour] = grouped.get(hour, 0) + 1
        except Exception:
            continue
    return grouped

def write_to_google_docs(report_text):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/documents"]
    )
    docs_service = build("docs", "v1", credentials=credentials)
    requests = [{"insertText": {"location": {"index": 1}, "text": report_text + "\n\n"}}]
    docs_service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()

def write_to_google_sheets(date_str, grouped, total):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    sheets_service = build("sheets", "v4", credentials=credentials)

    values = [[date_str, hour, count] for hour, count in sorted(grouped.items())]
    values.append(["", "Total do dia", total])

    body = {"values": values}

    sheets_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

if __name__ == "__main__":
    leads = load_new_leads()
    if not leads:
        print("⚠️ Nenhum novo lead para enviar ao relatório.")
    else:
        grouped = group_by_hour(leads)
        total = sum(grouped.values())

        date_str = datetime.now().strftime("%d/%m/%Y")
        report_lines = [f"📅 {date_str}"]
        for hour, count in sorted(grouped.items()):
            report_lines.append(f"🕓 {hour} → {count} leads")
        report_lines.append(f"\n👥 Total do dia: {total}\n")

        report_text = "\n".join(report_lines)
        print(report_text)

        write_to_google_docs(report_text)
        write_to_google_sheets(date_str, grouped, total)

        print("✅ Relatório atualizado no Google Docs e no Google Sheets (sem duplicar).")