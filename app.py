from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import pdfplumber
from docx import Document
import os, shutil, zipfile, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Resume Ranking API")

# ✅ Permanent storage folder (FIXED)
UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

stored_files = {}

# -------------------------------
# Extract text
# -------------------------------
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text_data = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                try:
                    text = page.extract_text()
                    if text:
                        text_data.append(text)
                except:
                    continue
        return " ".join(text_data)

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])

    return ""

# -------------------------------
# Clean text
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    return text

# -------------------------------
# Skills
# -------------------------------
skills_list = [
    "python","java","c","c++","sql","machine learning","deep learning",
    "nlp","tensorflow","pytorch","scikit-learn","matplotlib","seaborn",
    "pandas","numpy","aws","azure","google cloud","data analysis","data visualization"
]

def extract_skills(text):
    text = clean_text(text)
    return [s for s in skills_list if s in text]

def skill_score(jd, res):
    jd_s = extract_skills(jd)
    res_s = extract_skills(res)
    if not jd_s:
        return 0
    return round(len(set(jd_s) & set(res_s)) / len(jd_s) * 100, 2)

# -------------------------------
# Other Scores
# -------------------------------
def project_score(text):
    words = ["project","developed","built","created","implemented"]
    count = sum([text.count(w) for w in words])
    return 100 if count>=5 else 70 if count>=3 else 40 if count>=1 else 10

def experience_score(text):
    matches = re.findall(r'(\d+)\s+year', text)
    if matches:
        return min(int(max(matches))*20, 100)
    return 20

def calculate_score(jd,res):
    vec = TfidfVectorizer(stop_words='english')
    tfidf = vec.fit_transform([jd,res])
    return round(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]*100, 2)

# -------------------------------
# FRONTEND (UI FIXED)
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <head>
    <title>Resume Dashboard</title>
    <style>
        body {font-family: Arial; background:#f4f6f9; padding:30px;}
        h2 {text-align:center;}

        .upload-section {
        text-align:center;
        margin-bottom:50px;
    }

    textarea {
        width:70%;
        height:180px;
        font-size:16px;
        padding:12px;
        border-radius:10px;
        margin-bottom:20px;   /* 👈 SPACE BELOW JD */
    }

    .upload-section input {
        display:block;
        margin:15px auto;
    }

    button {
    background: #007bff;
    color: white;
    padding: 12px 25px;
    font-size: 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    margin-top: 15px;
    transition: 0.3s ease;
    }

    /* ✨ Hover effect */
    button:hover {
        background: #0056b3;
        transform: scale(1.05);
    }

    /*  Click effect */
    button:active {
        transform: scale(0.98);
    }

        .dashboard {
            width:70%;
            margin:auto;
        }

        .resume-card {
            background:#1c1c1c;
            color:white;
            padding:20px;
            margin-bottom:15px;
            border-radius:10px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        }

        .left {flex:2;}
        .right {
            flex:1;
            display:flex;
            justify-content:space-between;
            align-items:center;
        }

        .score {font-size:18px;}
        .high {color:#4caf50;}
        .medium {color:#ffeb3b;}
        .low {color:#f44336;}
    </style>
    </head>

    <body>
    <h2>Resume Ranking Dashboard</h2>

    <div class="upload-section">
        <textarea id="jdtext" placeholder="Paste Job Description here"></textarea><br>
        <input type="file" id="zipfile" accept=".zip"><br>
        <button onclick="upload()">Process Resumes</button>
    </div>

    <div class="dashboard" id="dashboard"></div>

    <script>
    function getClass(score){
        if(score>60) return "high";
        else if(score>=40) return "medium";
        return "low";
    }

    async function upload(){
        const jd = document.getElementById("jdtext").value;
        const zip = document.getElementById("zipfile").files[0];

        if(!jd || !zip){
            alert("Provide JD + ZIP!");
            return;
        }

        const fd = new FormData();
        fd.append("jd_text", jd);
        fd.append("zip_file", zip);

        const dash = document.getElementById("dashboard");
        dash.innerHTML="Processing...";

        const res = await fetch("/upload-resumes-zip/", {method:"POST", body:fd});
        const data = await res.json();

        dash.innerHTML="";

        data.results.forEach((r,i)=>{
            const card=document.createElement("div");
            card.className="resume-card";

            const left=document.createElement("div");
            left.className="left";

            const right=document.createElement("div");
            right.className="right";

            const name=document.createElement("span");
            name.innerText=`#${i+1} ${r.file}`;

            const score=document.createElement("span");
            score.innerText=r.final_score+"%";
            score.className="score "+getClass(r.final_score);

            const btn=document.createElement("button");
            btn.innerText="View Resume";
            btn.onclick=()=>window.open("/view/"+r.file, "_blank");

            left.appendChild(name);
            right.appendChild(score);
            right.appendChild(btn);

            card.appendChild(left);
            card.appendChild(right);
            dash.appendChild(card);
        });
    }
    </script>
    </body>
    </html>
    """

# -------------------------------
# VIEW RESUME (FIXED)
# -------------------------------
@app.get("/view/{filename}")
async def view_resume(filename: str):
    file_path = stored_files.get(filename)

    if file_path and os.path.exists(file_path):
        return FileResponse(file_path)

    return JSONResponse({"error": "File not found"}, status_code=404)

# -------------------------------
# PROCESS ZIP (FIXED)
# -------------------------------
@app.post("/upload-resumes-zip/")
async def upload_resumes_zip(jd_text: str = Form(...), zip_file: UploadFile = File(...)):
    global stored_files
    stored_files = {}

    results = []

    # Save zip permanently
    zip_path = os.path.join(UPLOAD_DIR, zip_file.filename)

    with open(zip_path, "wb") as f:
        shutil.copyfileobj(zip_file.file, f)

    # Extract zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_DIR)

    jd_clean = clean_text(jd_text)

    for root, _, files in os.walk(UPLOAD_DIR):
        for f_name in files:
            if f_name.endswith((".pdf",".docx")):
                path = os.path.join(root, f_name)

                stored_files[f_name] = path  # ✅ FIXED

                text = extract_text(path)
                text_clean = clean_text(text)

                keyword = calculate_score(jd_clean,text_clean)
                skills = skill_score(jd_clean,text_clean)
                proj = project_score(text_clean)
                exp = experience_score(text_clean)

                final = 0.4*keyword + 0.3*skills + 0.2*proj + 0.1*exp

                results.append({
                    "file": f_name,
                    "final_score": round(final,2)
                })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    return JSONResponse({"results": results})
