# AI-Powered-Resume-Screening-and-Candidate-Ranking-System-for-Recruiters
Link Of project after deployment : https://ai-resume-ranking-app.onrender.com
## 🔥 Overview
This is an advanced **FastAPI-based Resume Screening System** that automatically ranks candidates based on a Job Description (JD) using **semantic similarity (Sentence Transformers)**, skill matching, and heuristic scoring.

It processes resumes (PDF/DOCX inside ZIP files), extracts meaningful text, and ranks candidates using AI-powered semantic understanding.

---

## 🧠 Key Features
- Upload Job Description (JD)
- Upload ZIP file containing multiple resumes
- Extract text from PDF and DOCX files
- AI-powered semantic similarity scoring (Sentence Transformers)
- TF-IDF alternative replaced with **MiniLM transformer model**
- Skill-based scoring system
- Project experience scoring
- Experience extraction scoring
- Chunk-based semantic comparison for better accuracy
- Interactive web dashboard
- Resume viewer in browser

---

## 🏗️ Tech Stack
- FastAPI
- Python 3.10+
- SentenceTransformers (`all-MiniLM-L6-v2`)
- PyTorch (backend for embeddings)
- Scikit-learn (for supporting logic)
- PDFPlumber
- python-docx
- HTML, CSS, JavaScript

---

## 📁 Project Structure
uploaded_resumes/ # Stored resumes after upload
app.py # Main FastAPI backend
backend_logic.py # Supporting logic (if used)
fastapi_wrap_backend.py
resumes.zip # Sample dataset
requirements.txt
start.sh

---

## ⚙️ How It Works

### 1. Input Stage
- User enters Job Description (JD)
- Uploads ZIP file containing resumes

---

### 2. Resume Processing
- ZIP file is extracted
- Each resume is parsed (PDF/DOCX)
- Text is cleaned and normalized

---

### 3. AI Scoring System

Each resume is evaluated using multiple scoring methods:

---

### 🔹 1. Semantic Similarity Score (MAIN AI COMPONENT 🚀)
- Uses `SentenceTransformer('all-MiniLM-L6-v2')`
- Converts JD and resume chunks into embeddings
- Computes cosine similarity

✔ Advantages:
- Understands meaning, not just keywords
- Matches synonyms and context
- Much more accurate than TF-IDF

---

### 🔹 2. Skill Matching Score
Matches predefined skills:
- Python, Java, SQL, AWS, Machine Learning, Deep Learning, etc.

---

### 🔹 3. Project Score
Based on keywords:
- built, developed, created, implemented

---

### 🔹 4. Experience Score
Extracts years of experience using regex patterns

---

## ⚖️ Final Score Formula

```python
final_score = (
    0.4 * semantic_score +
    0.3 * skill_score +
    0.2 * project_score +
    0.1 * experience_score
)

##🌐 API Endpoints
🔹 Home Page
GET /
Loads interactive resume ranking dashboard
🔹 Upload Resumes
POST /upload-resumes-zip/

Input:

jd_text → Job Description
zip_file → ZIP file of resumes

Output:

Ranked list of resumes with scores
🔹 View Resume
GET /view/{filename}
Opens resume directly in browser

##🎨 Frontend Features
JD input box
ZIP upload input
"Process Resumes" button
Dynamic ranked cards
Color-coded scores:
🟢 High (>60)
🟡 Medium (40–60)
🔴 Low (<40)
"View Resume" button per candidate
##Create 3 files in Github
AI-Powered-Resume-Screening-and-Candidate-Ranking-System-for-Recruiters/
│
├── app.py
├── backend_logic.py
├── fastapi_wrap_backend.py
├── requirements.txt   ✅ (you create)
├── runtime.txt        ✅ (you create)
├── start.sh           ✅ (you create)
├── README.md
└── .gitignore
🌸 STEP-BY-STEP (do exactly this)
✅ Step 1 — Create files locally

Inside your project folder:

1. Create requirements.txt

👉 Right click → New file → paste:

fastapi
uvicorn
pdfplumber
python-docx
scikit-learn
sentence-transformers
torch
python-multipart

2. Create runtime.txt
python-3.10.0

3. Create start.sh
uvicorn app:app --host 0.0.0.0 --port 10000
##Deploy on Render

Go to 👉 https://render.com

Then:

Click New +
Choose Web Service --> Choose one repo click
Connect your GitHub repo
👉 AI-Powered-Resume-Screening-and-Candidate-Ranking-System-for-Recruiters
STEP 1 — Select your repo

👉 Click this:

Rin-ui / AI-Powered-Resume-Screening-and-Candidate-Ranking-System-for-Recruiters
🌸 STEP 2 — Choose service type

Render will ask:

👉 Select Web Service

🌸 STEP 3 — Fill configuration (VERY IMPORTANT)

You’ll now see a form — fill it like this:

🔹 Name
ai-resume-ranking-app
🔹 Region

👉 Leave default (or closest to you)

🔹 Branch
main
🔹 Runtime / Environment

👉 Select:

Python 3
🔹 Build Command

Paste:

pip install -r requirements.txt
🔹 Start Command

Paste:

bash start.sh
🌸 STEP 4 — Advanced settings (skip)

👉 Don’t change anything else
(default is fine)

🌸 STEP 5 — Deploy

👉 Click:

Create Web Service
⏳ STEP 6 — Wait
First deploy takes 5–10 minutes
You’ll see logs running

👉 Look for:

==> Your service is live 🎉
🌸 STEP 7 — Open your app

You’ll get a link like:

https://resume-ranking-app.onrender.com

👉 Click it → your dashboard opens 💙

⚠️ Limitations
First deployment may take time due to model loading
Large ZIP files may slow processing
Free tier may sleep after inactivity
🌟 Future Improvements
Add GPU-based embeddings for faster inference
Use PostgreSQL database for resume storage
Add authentication system for recruiters
Add background task queue (Celery / Redis)
Improve ranking with fine-tuned transformer model

💼 Project Summary

This system is an AI-powered resume ranking engine that uses semantic understanding (transformers) to match candidates with job descriptions more accurately than traditional keyword-based systems.
