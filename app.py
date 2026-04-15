from flask import Flask, render_template, request
import pdfplumber
from docx import Document
import spacy
import re
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Extract text
def extract_text(file):
    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return "".join(page.extract_text() for page in pdf.pages)
    
    elif file.filename.endswith('.docx'):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

# Extract details
def extract_email(text):
    match = re.search(r'\S+@\S+', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'\b\d{10}\b', text)
    return match.group() if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

def extract_skills(text):
    skills = ["python", "java", "sql", "machine learning"]
    return [skill for skill in skills if skill in text.lower()]

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        text = extract_text(file)

        data = {
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text)
        }

        return render_template("index.html", data=data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)