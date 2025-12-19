from flask import Flask, render_template, request
import os
from utils import extract_text_from_pdf, clean_text, rank_resumes

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "resumes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []

    if request.method == 'POST':
        job_desc_input = request.form.get('job_desc')

        if not job_desc_input:
            return render_template(
                'index.html',
                error="Please enter Job Description"
            )

        job_desc = clean_text(job_desc_input)

        files = request.files.getlist('resumes')

        resume_texts = []
        resume_names = []

        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            text = extract_text_from_pdf(path)
            resume_texts.append(clean_text(text))
            resume_names.append(file.filename)

        scores = rank_resumes(resume_texts, job_desc)

        results = sorted(
            zip(resume_names, scores),
            key=lambda x: x[1],
            reverse=True
        )

    return render_template('index.html', results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


