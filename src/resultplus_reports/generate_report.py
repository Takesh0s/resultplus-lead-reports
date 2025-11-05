"""
generate_report.py
==================

Generates and updates daily lead reports in **Google Docs** and **Google Sheets**
using a Google Cloud service account for authentication.

Main workflow:
1. Load new leads from `leads.json`, avoiding duplicates with `sent.json`.
2. Group leads by creation hour.
3. Write a formatted summary to Google Docs.
4. Append detailed data to Google Sheets.

Requirements:
- Service account key file: `gcp-key.json`
- Environment variables in `.env`:
    - `SPREADSHEET_ID`: Google Sheets spreadsheet ID
    - `DOC_ID`: Google Docs document ID

Outputs:
- Updates the daily report in Google Docs.
- Appends a new set of rows to Google Sheets (one per hour + daily total).
"""

import os
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths and identifiers
SERVICE_ACCOUNT_FILE = "gcp-key.json"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
DOC_ID = os.getenv("DOC_ID")


def load_new_leads():
    """
    Loads leads from `leads.json` and returns only new entries
    that have not been sent yet. Updates `sent.json` accordingly.

    Returns:
        list[dict]: List of new leads to be processed.
    """
    if not os.path.exists("leads.json"):
        print("⚠️ No leads.json file found.")
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

    # Update sent.json with processed IDs
    sent_ids.update([l["id"] for l in new_leads])
    with open("sent.json", "w", encoding="utf-8") as f:
        json.dump(list(sent_ids), f, ensure_ascii=False, indent=2)

    return new_leads


def group_by_hour(leads):
    """
    Groups leads by creation hour (local timezone).

    Args:
        leads (list[dict]): List of lead dictionaries with "criado_em" field.

    Returns:
        dict[str, int]: Mapping of hour → lead count.
    """
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
    """
    Inserts the given report text at the top of a Google Docs document.

    Args:
        report_text (str): Formatted report text.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/documents"]
    )
    docs_service = build("docs", "v1", credentials=credentials)

    requests = [{"insertText": {"location": {"index": 1}, "text": report_text + "\n\n"}}]
    docs_service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()


def write_to_google_sheets(date_str, grouped, total):
    """
    Appends lead data to a Google Sheets spreadsheet,
    including per-hour counts and daily total.

    Args:
        date_str (str): Report date in dd/mm/yyyy format.
        grouped (dict): Mapping of hour → lead count.
        total (int): Total number of leads for the day.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    sheets_service = build("sheets", "v4", credentials=credentials)

    values = [[date_str, hour, count] for hour, count in sorted(grouped.items())]
    values.append(["", "Daily total", total])

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
        print("⚠️ No new leads to include in the report.")
    else:
        grouped = group_by_hour(leads)
        total = sum(grouped.values())

        date_str = datetime.now().strftime("%d/%m/%Y")
        report_lines = [f"📅 {date_str}"]
        for hour, count in sorted(grouped.items()):
            report_lines.append(f"🕓 {hour} → {count} leads")
        report_lines.append(f"\n👥 Total leads of the day: {total}\n")

        report_text = "\n".join(report_lines)
        print(report_text)

        write_to_google_docs(report_text)
        write_to_google_sheets(date_str, grouped, total)

        print("✅ Report successfully updated in Google Docs and Google Sheets (no duplicates).")