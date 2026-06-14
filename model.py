import spacy
import pdfplumber
from docx import Document
import re

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# -----------------------------------
# Text Extraction
# -----------------------------------
def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text


# -----------------------------------
# Skill Extraction
# -----------------------------------
SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "nlp", "spacy", "tensorflow", "pytorch", "sql", "data analysis",
    "project management", "communication", "teamwork", "leadership",
    "problem-solving", "critical thinking", "creativity", "adaptability"
]

def extract_skills(text):
    found_skills = []
    text_lower = text.lower()
    for skill in SKILLS_DB:
        if skill in text_lower:
            found_skills.append(skill)
    return found_skills

def skill_similarity(skills1, skills2):
    if not skills1 or not skills2:
        return 0.0
    return round(
        (len(set(skills1) & set(skills2)) / len(set(skills1) | set(skills2))) * 100,
        2
    )



# -----------------------------------
# Education Extraction
# -----------------------------------
DEGREES = ["b.tech", "m.tech", "B.E", "M.E", "bachelor", "master", "phd", "b.sc", "m.sc", "b.a", "m.a", "associate", "doctorate"]

def extract_education(text):
    text = text.lower()
    return list(set([d for d in DEGREES if d in text]))


# -----------------------------------
# Semantic Similarity
# -----------------------------------
def resume_similarity(text1, text2):
    if len(text1.strip()) < 200 or len(text2.strip()) < 200:
        return 0.0
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return round(doc1.similarity(doc2) * 100, 2)



# -----------------------------------
# Resume Comparison Function
# -----------------------------------
def compare_resumes(original_resume, sample_resume):

    text_original = extract_text(original_resume)
    text_sample = extract_text(sample_resume)

    similarity_score = resume_similarity(text_original, text_sample)

    extracted_skills_original = extract_skills(text_original)
    extracted_skills_sample = extract_skills(text_sample)

    skill_match_percentage = skill_similarity(extracted_skills_original, extracted_skills_sample)

    edu_original = extract_education(text_original)
    edu_sample = extract_education(text_sample)

    skill_match = set(extracted_skills_original).intersection(set(extracted_skills_sample))

    overall_score = (similarity_score + skill_match_percentage) / 2

    result = {
        "Similarity Percentage": f"{overall_score} %",
        "Skill Match Percentage": f"{skill_match_percentage} %",
        "Original Skills": extracted_skills_original,
        "Sample Skills": extracted_skills_sample,
        "Matched Skills": list(skill_match),
        "Original Education": edu_original,
        "Sample Education": edu_sample,
        "Status": "Copied / Highly Similar ❌" if similarity_score > 75 else "Genuine Resume ✅"
    }

    if overall_score >= 50:
        result["Overall Verdict"] = "Selected"
    else:
        result["Overall Verdict"] = "Rejected"


    return result


# -----------------------------------
# Run Example
# -----------------------------------
if __name__ == "__main__":
    output = compare_resumes(
        "/content/original_resume.pdf",
        "/content/sample_resume.pdf"
    )

    print("\n===== RESUME COMPARISON REPORT =====")

    for k, v in output.items():
        print(f"{k}: {v}")