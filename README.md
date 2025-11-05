# 📊 ResultPlus Lead Reports

Automated lead report generator built during my internship at **ResultPlus**, a company using the **Helena CRM White-Label** system.

This project automates the process of **collecting, validating, and reporting leads** from marketing campaigns — replacing a manual workflow that was prone to errors and delays.

---

## 🧠 Overview

After an issue with AWS infrastructure caused inconsistencies between **Meta Ads** and **CRM reports**, the marketing team needed a reliable and automated way to verify the number of leads captured by each campaign.

This system connects to the **Helena CRM API**, fetches all chat sessions, filters recent and valid ones, and automatically generates reports in **Google Sheets** and **Google Docs** for daily validation.

---

## ⚙️ Core Features

- 🔄 **Automated data collection** from Helena CRM (private API)
- 📑 **Report generation** in Google Sheets and Google Docs
- 🧩 **Environment variable management** via `.env`
- 🔐 **Google Cloud integration** using service account credentials
- 🧪 **Diagnostic scripts** for testing API endpoints, pagination, and hidden sessions
- 🧱 **Modular architecture**, easy to extend to new CRM endpoints

---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| Language | Python |
| API Client | `requests` |
| Cloud Integration | `google-api-python-client`, `google-auth` |
| Secrets Management | `python-dotenv` |
| Formatting | `json`, `datetime`, `os` |

---

## 🧱 Project Structure

resultplus-reports/
├── fetch_result.py → Fetches data from Helena CRM
├── generate_report.py → Creates and updates reports in Google Docs/Sheets
├── find_hidden_sessions.py → Tests for hidden sessions in the API
├── find_real_swagger_json.py → Attempts to discover actual API endpoints
├── scan_api_swagger.py → Scans the Swagger specification
├── scan_swagger.py → Additional endpoint analysis
├── test_endpoints.py → Verifies endpoint accessibility
├── test_pagination.py → Tests pagination behavior in responses
├── test_query_params.py → Validates query parameters for filtering
├── test_search_post.py → Tests POST endpoints for search operations
├── requirements.txt → Dependencies
├── .env → Environment variables (ignored via .gitignore)
├── gcp-key.json → Google Cloud credentials (ignored via .gitignore)
└── .gitignore → Excludes sensitive/local files

---

## 🧾 Example Workflow

1. **Set up environment variables**  
   Fill your `.env` file with required API tokens and Google document IDs.

2. **Run data collection**  
   ```bash
   python fetch_result.py

3. **Generate report automatically**  
   python generate_report.py

4. **Access generated reports**  
   Reports are automatically published and updated in Google Sheets and Google Docs.


---

## 🔒 Security

Sensitive files are not included in this repository for safety:

.env
gcp-key.json
leads.json
sent.json

These files are listed in .gitignore and must be created locally when running the project.