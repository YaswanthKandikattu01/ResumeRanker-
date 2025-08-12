# Resume Automation with AI + Google Workspace

An advanced Python tool that automates resume screening, scoring, and organization using OpenAI GPT, Google Sheets API, and Google Drive API.

## ✨ Features
- Batch process PDF resumes
- AI-powered extraction of candidate details & skills
- Match scoring against a job description
- Auto-generated summaries & match percentages
- Google Sheets integration for structured tracking
- Google Drive upload with organized folders
- Local CSV backups & shortlist generation

---

## 📦 Installation & Setup

### 1. Install Required Software
- [Python 3.10+](https://www.python.org/downloads/) (check “Add Python to PATH” on Windows)
- [Visual Studio Code](https://code.visualstudio.com/) with Python extension
- (Optional) [Git](https://git-scm.com/downloads)

### 2. Get the Code
- Download and unzip `resume-automation-advanced.zip` **OR** clone from GitHub:
```bash
git clone https://github.com/yourusername/resume-automation.git
```
- Open the folder in VS Code.

### 3. Create Virtual Environment
**Windows**
```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```
**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys & Credentials

### OpenAI API Key
1. Get key from [platform.openai.com](https://platform.openai.com/) → API Keys.
2. Save as environment variable:
   - **Windows**:
     ```powershell
     $env:OPENAI_API_KEY="sk-yourkey"
     ```
   - **macOS/Linux**:
     ```bash
     export OPENAI_API_KEY="sk-yourkey"
     ```

### Google Sheets API
1. In [Google Cloud Console](https://console.cloud.google.com/), create a new project.
2. Enable **Google Sheets API** and **Google Drive API**.
3. Create Service Account → Role: **Editor**.
4. Download JSON key → save as `gspread_credentials.json` in the project folder.
5. Share your Google Sheet with the `"client_email"` from the JSON.

### Google Drive OAuth Client
1. Create OAuth client ID → Application type: **Desktop app**.
2. Download JSON → save as `client_secrets.json` in the project folder.

---

## 📋 Configure Spreadsheet ID
From your Google Sheet URL:
```
https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit
```
Copy the part between `/d/` and `/edit` and:
- Add it to `main.py` under:
```python
SPREADSHEET_ID = "your-id-here"
```
OR
- Export as environment variable:
```bash
export SPREADSHEET_ID="your-id-here"
```

---

## 📂 Add Resumes
Place all candidate PDF files in the `resumes/` folder.

---

## ▶ Run the Program
```bash
python main.py
```
- On first run, a browser window will ask for Google Drive permissions.
- After processing, check:
  - **Google Sheet** for structured candidate data
  - **Google Drive** for uploaded resumes
  - **output.csv** for local backup & shortlist

---

## 🛠 Tech Stack
- Python 3.10+
- OpenAI GPT
- Google Sheets API & Drive API
- pdfplumber, gspread, PyDrive2

---

## 📜 License
MIT License
