# Advanced Resume Automation Workflow (Python Version of n8n)

## Features
- Batch process multiple resumes from a folder
- Upload to Google Drive
- Extract text & personal info using OpenAI
- Summarize and HR evaluate candidates
- Keyword matching against job description
- Rank candidates by score
- Local CSV backup of results

## Setup
1. Create Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Place credentials:
- `gspread_credentials.json` for Google Sheets
- `client_secrets.json` for Google Drive
- Share your Google Sheet with the service account email.

4. Set environment variables:
```bash
export OPENAI_API_KEY="paster your_key_here"   # Mac/Linux
setx OPENAI_API_KEY "your_key_here"     # Windows PowerShell
```

5. Edit `paste your SPREADSHEET_ID` in `main.py`.

6. Place resumes in `resumes/` folder.

7. Run the script:
```bash
python main.py
```
