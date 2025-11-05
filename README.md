# 📊 ResultPlus Lead Reports

Automated diagnostic and reporting toolkit built during my internship at **ResultPlus**, a company using the **Helena CRM White-Label** system.

This project was designed to automate the process of **collecting, validating, and reporting leads** from marketing campaigns — replacing a manual workflow that was prone to human error and data delays.

---

## 🧠 Background

During development, the **Helena CRM API** presented a major limitation: it only exposed session data up to **September 1st**, regardless of more recent activity.  
Because of this, several **diagnostic and endpoint exploration scripts** were created to probe alternative URLs, Swagger specifications, and hidden routes that could reveal more recent data.

Even with these restrictions, the system successfully:
- Automated **lead data collection** within the accessible date range;
- Generated **structured JSON reports** and **Google Docs/Sheets summaries**;
- Provided a **reproducible and transparent** process for lead validation.

---

## ⚙️ Core Features

- 🔄 **Automated data fetching** from Helena CRM (private API)
- 🧪 **Diagnostic utilities** to explore hidden or undocumented endpoints
- 📊 **Report generation** using Google Sheets and Google Docs APIs
- 🧩 **Environment management** via `.env` and service account keys
- 🧱 **Modular and package-based architecture**
- 🕒 **Timestamped output files** for traceability and auditability

---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| Language | Python 3.10+ |
| HTTP Client | `requests` |
| Cloud Integration | `google-api-python-client`, `google-auth` |
| Environment | `python-dotenv` |
| Utilities | `datetime`, `logging`, `os`, `json` |

---

## 🧱 Project Structure

```bash
resultplus-reports/
├── src/
│ └── resultplus_reports/
│ ├── init.py → Package initialization and metadata
│ ├── main.py → Entry point for python -m resultplus_reports
│ ├── fetch_result.py → Fetches data from Helena CRM
│ ├── generate_report.py → Generates reports in Google Docs/Sheets
│ ├── find_hidden_sessions.py → Tests for hidden session endpoints
│ ├── find_real_swagger_json.py → Attempts to locate the true Swagger/OpenAPI JSON
│ ├── scan_api_swagger.py → Scans API for possible hidden routes
│ ├── scan_swagger.py → Additional endpoint analysis
│ ├── test_endpoints.py → Verifies endpoint accessibility
│ ├── test_pagination.py → Tests pagination response behavior
│ ├── test_query_params.py → Validates query parameters
│ └── test_search_post.py → Tests POST search endpoints
├── requirements.txt → Python dependencies
├── pyproject.toml → Package metadata and build system
├── .env → Environment variables (ignored via .gitignore)
├── gcp-key.json → Google Cloud credentials (ignored via .gitignore)
└── .gitignore → Excludes sensitive/local files
```

---

## 🧾 Example Workflow

1. **Set up your environment variables**

   Create a `.env` file containing:
   ```
   HELENA_API_KEY=...
   GOOGLE_SHEET_ID=...
   GOOGLE_DOC_ID=...
   ```

2. **Run data fetching**
   ```bash
   python -m resultplus_reports
   # or explicitly:
   python src/resultplus_reports/fetch_result.py
   ```

3. **Generate the report**
   ```bash
   python src/resultplus_reports/generate_report.py
   ```

4. **Access the generated files**

   - Leads are saved as `leads_YYYYMMDD.json`
   - Reports are automatically synced to Google Sheets and Docs

---

## 🔍 Diagnostics

Due to API restrictions, the following tools were developed to explore alternative data sources and confirm endpoint behavior:

- `find_hidden_sessions.py` — probes multiple session-related routes for recent data  
- `find_real_swagger_json.py` — discovers actual Swagger/OpenAPI references  
- `scan_api_swagger.py` and `scan_swagger.py` — inspect and parse endpoint metadata  
- `test_*.py` scripts — validate request limits, pagination, and query filtering

These diagnostics ensured that every possible data retrieval method was tested and documented — even under restrictive API conditions.

---

## 🔒 Security

Sensitive configuration files are intentionally excluded:

```
.env  
gcp-key.json  
leads_*.json  
sent.json
```

All are listed in `.gitignore` and must be created locally when executing the project.

---

## 🏁 Version

**v1.0.0** — stable, archived release.  
This version reflects the final working state of the system before API access was restricted by the Helena platform.

---

## 👨‍💻 Author

**Luiz Phillipe (Takeshi)**  
🔗 [github.com/Takesh0s](https://github.com/Takesh0s)

Developed during my internship at **ResultPlus**, later refined and published for **educational and portfolio purposes**.