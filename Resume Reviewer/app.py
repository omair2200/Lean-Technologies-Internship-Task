import os
import io
from flask import Flask, render_template, request, abort, jsonify
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text
from openai import OpenAI
import re
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['TEXT_OUTPUT_PATH'] = 'uploads/pdf'

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def convert_pdf_to_text(resume, text_path):
    with io.BytesIO(resume) as pdf_file:
        text = extract_text(pdf_file)
        with open(text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

def get_review(resume, target_profile):
    text_content = extract_text(io.BytesIO(resume))
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "user",
            "content": f"Hello ChatGPT, I hope this message finds you well. I'm currently refining my resume for the {target_profile} and would greatly appreciate your detailed and curated feedback.Before we proceed with the section-wise analysis, could you kindly rate the overall effectiveness of the resume based on the following metrics, each on a scale of 1 to 10:1. Clarity and Conciseness: How effectively does the resume communicate my qualifications and experiences tailored to the {target_profile}? Is the information presented in a clear and concise manner, emphasizing relevant skills and experiences for this role?2. Relevance and Alignment: Does the resume effectively align with the requirements and expectations of the {target_profile}? Are the skills and experiences highlighted directly relevant to the desired positions within this industry?3. Impact and Achievement: To what extent does the resume showcase my achievements and contributions in previous roles, specifically related to the {target_profile}? Does it effectively highlight my accomplishments and the value I can bring to potential employers in this field?4. Professionalism and Presentation: How polished and professional does the resume appear in terms of formatting, design, and overall presentation, tailored to the standards of the {target_profile}? Does it make a strong visual impression consistent with expectations in this industry?5. Grammar and Language: Are there any grammatical errors or language issues that detract from the clarity and professionalism of the resume for the {target_profile}? Is the language used appropriate and effective for the intended audience within this industry?Additionally, I would appreciate a curated and detailed analysis of each section with insights tailored to the requirements of the {target_profile}. Please provide longer explanations, focusing on areas for improvement and any grammatical mistakes or language issues you identify within the context of this industry. Your comprehensive insights will be invaluable in helping me refine and improve my resume for the {target_profile}. Thank you for your time and expertise; I eagerly await your review.{text_content}"
        }
    ],
    )
  
    response_content = chat_completion.choices[0].message.content
    formatted_response = response_content.replace('\n', '<br>')
    formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_response) 
    return formatted_response

@app.route('/', methods=['GET', 'POST'])
def index():
    review = None

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        target_profile = request.form.get('profile')
        if not uploaded_file:
            abort(400, 'No file part')

        filename = secure_filename(uploaded_file.filename)

        if filename:
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400, 'Invalid file extension')

            resume = uploaded_file.read()

            review = get_review(resume, target_profile)

            return jsonify({'review': review})

    return render_template('index.html', review=review)

if __name__ == "__main__":
    app.run(debug=True)
