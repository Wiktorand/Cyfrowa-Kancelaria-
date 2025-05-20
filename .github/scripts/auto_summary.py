import os
import openai
import pdfplumber
from docx import Document

openai.api_key = os.getenv("OPENAI_API_KEY")

FOLDERS = ["Cywilna", "Apelacja", "Egzekucja"]

def extract_text_from_pdf(path):
    try:
        with pdfplumber.open(path) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        return f"(Błąd odczytu PDF: {e})"

def extract_text_from_docx(path):
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"(Błąd odczytu DOCX: {e})"

def summarize(text, filename, folder):
    prompt = (
        f"Jesteś elitarnym zespołem prawników AI Cyfrowej Kancelarii Wiktora Andrukiewicza z Wrocławia. "
        f"Streszcz poniższy dokument ({filename}) z folderu {folder} w 5-10 zdaniach, podkreślając kluczowe fakty, argumenty i znaczenie dla sprawy. "
        f"Zachowaj styl profesjonalny i zgodny z wytycznymi kancelarii. Oto treść dokumentu:\n\n{text[:12000]}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=600
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"(Błąd generowania streszczenia: {e})"

for folder in FOLDERS:
    folder_path = os.path.join(os.getcwd(), folder)
    if not os.path.isdir(folder_path):
        continue

    summaries = []
    for fname in os.listdir(folder_path):
        if fname.lower() in ["knowledge.md", "reader.txt", "readme.md"]:
            continue
        fpath = os.path.join(folder_path, fname)
        if not os.path.isfile(fpath):
            continue

        # Sprawdź, czy streszczenie już istnieje w knowledge.md
        summary_tag = f"### {fname}"
        knowledge_path = os.path.join(folder_path, "knowledge.md")
        if os.path.exists(knowledge_path):
            with open(knowledge_path, "r", encoding="utf-8") as kf:
                if summary_tag in kf.read():
                    continue  # już podsumowane

        # Ekstrakcja tekstu
        if fname.lower().endswith(".pdf"):
            text = extract_text_from_pdf(fpath)
        elif fname.lower().endswith(".docx"):
            text = extract_text_from_docx(fpath)
        else:
            continue

        # Generowanie streszczenia
        summary = summarize(text, fname, folder)
        summaries.append(f"### {fname}\n{summary}\n")

    # Dopisz nowe streszczenia do knowledge.md
    if summaries:
        with open(os.path.join(folder_path, "knowledge.md"), "a", encoding="utf-8") as kf:
            kf.write("\n".join(summaries))
