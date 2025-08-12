import os
import datetime
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pdfplumber
import pandas as pd

# CONFIG
openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_SHEETS_CREDENTIALS_FILE = "gspread_credentials.json"
GOOGLE_DRIVE_CREDENTIALS_FILE = "client_secrets.json"
SPREADSHEET_ID = "your_spreadsheet_id_here"
RESUME_FOLDER = "resumes"
JOB_DESCRIPTION = """We are a web agency looking for an Automation Expert skilled in workflow automation, API integrations, and AI-driven process optimization."""

# GOOGLE SHEETS SETUP
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# GOOGLE DRIVE SETUP
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# FUNCTIONS
def upload_to_drive(file_path, file_name):
    file_drive = drive.CreateFile({'title': file_name})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    return file_drive['id']

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_personal_info(text):
    prompt = f"Extract first name, last name, email, city, birthdate, skills, website, education, experience from:\n{text}\nReturn in JSON."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def summarize_candidate(info):
    prompt = f"Write a professional summary in under 100 words for:\n{info}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def hr_evaluation(profile, candidate_summary):
    prompt = f"You are an HR expert. Compare this profile:\n{profile}\nWith candidate:\n{candidate_summary}\nRate 1-10 and explain why."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

def keyword_match_percentage(job_description, resume_text):
    job_keywords = set(job_description.lower().split())
    resume_words = set(resume_text.lower().split())
    matches = job_keywords & resume_words
    return round((len(matches) / len(job_keywords)) * 100, 2)

def append_to_sheet(data):
    sheet.append_row(data)

# MAIN WORKFLOW
if __name__ == "__main__":
    results = []
    for filename in os.listdir(RESUME_FOLDER):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(RESUME_FOLDER, filename)
            print(f"Processing: {filename}")
            
            uploaded_id = upload_to_drive(file_path, f"{filename}-{datetime.date.today()}.pdf")
            resume_text = extract_text_from_pdf(file_path)
            personal_info = extract_personal_info(resume_text)
            summary = summarize_candidate(personal_info)
            evaluation = hr_evaluation(JOB_DESCRIPTION, summary)
            keyword_score = keyword_match_percentage(JOB_DESCRIPTION, resume_text)
            
            # Example score extraction (basic placeholder)
            try:
                score = int([s for s in evaluation.split() if s.isdigit()][0])
            except:
                score = 0
            
            row = [filename, personal_info, summary, evaluation, keyword_score, str(datetime.date.today())]
            append_to_sheet(row)
            results.append({"filename": filename, "score": score, "keyword_score": keyword_score})
    
    # Sort and display top candidates
    df = pd.DataFrame(results)
    df = df.sort_values(by=["score", "keyword_score"], ascending=False)
    df.to_csv("results_backup.csv", index=False)
    print("Top candidates:\n", df.head())
