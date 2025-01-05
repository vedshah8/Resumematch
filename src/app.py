import spacy
import pdfplumber
import re
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request

app = Flask(__name__)

nlp = spacy.load("output/model-best")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

def match_skills(skills_text, resume_skills_list):
    resume_embedding = get_bert_embeddings(skills_text)
    matched_skills = []

    for skill in resume_skills_list:
        skill_embedding = get_bert_embeddings(skill)
        similarity = cosine_similarity([resume_embedding], [skill_embedding])[0][0]
        if similarity > 0.5:
            matched_skills.append(skill)

    return matched_skills

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_skills_from_jd(jd_text):
    skills_pattern = re.compile(r"(?i)(skills|requirements|must\s+have|desired\s+skills|required\s+skills|key\s+competencies):?\s*(.*?)(?=\n\n|\n\w+?:|\Z)", re.DOTALL)
    skills_match = skills_pattern.search(jd_text)
    if skills_match:
        return skills_match.group(2).strip()
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    resume_file = request.files['resume']
    jd_file = request.files['jd']

    resume_text = extract_text_from_pdf(resume_file)
    jd_text = extract_text_from_pdf(jd_file)

    doc = nlp(resume_text)
    resume_skills_list = []
    for ent in doc.ents:
        resume_skills_list.append(ent.text)
    skills_text = extract_skills_from_jd(jd_text)
    matched_skills = match_skills(skills_text, resume_skills_list)
    
    return render_template('results.html', matched_skills=matched_skills)

if __name__ == '__main__':
    app.run(debug=True)
