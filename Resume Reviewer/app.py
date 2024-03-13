import os
import io
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
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

def convert_pdf_to_text(pdf_content, text_path):
    with io.BytesIO(pdf_content) as pdf_file:
        text = extract_text(pdf_file)
        with open(text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

def get_chatgpt_response(pdf_content):
    text_content = extract_text(io.BytesIO(pdf_content))
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "user",
            "content": f" Hello ChatGPT, I hope this message finds you well. I'm currently refining my resume and would greatly appreciate your detailed and comprehensive feedback. Before we proceed with the section-wise analysis, could you kindly rate the overall effectiveness of the resume based on the following metrics, each on a scale of 1 to 10:1. Clarity and Conciseness: How effectively does the resume communicate my qualifications and experiences? Is the information presented in a clear and concise manner?2. Relevance and Alignment: Does the resume effectively align with the requirements and expectations of the targeted roles and industries? Are the skills and experiences highlighted relevant to the desired positions?3. Impact and Achievement: To what extent does the resume showcase my achievements and contributions in previous roles? Does it effectively highlight my accomplishments and the value I can bring to potential employers?4. Professionalism and Presentation: How polished and professional does the resume appear in terms of formatting, design, and overall presentation? Does it make a strong visual impression?5. Grammar and Language: Are there any grammatical errors or language issues that detract from the clarity and professionalism of the resume? Is the language used appropriate and effective for the intended audience?Once you've provided your ratings for these metrics, we can proceed with a more detailed analysis of each section. Your comprehensive insights will be invaluable in helping me refine and improve my resume. Thank you for your time and expertise; I eagerly await your review.{text_content}"
        }
    ],
    )
    # Access the response content
    response_content = chat_completion.choices[0].message.content
    formatted_response = response_content.replace('\n', '<br>')  # Convert line breaks to HTML line breaks
    formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_response)  # Bold enclosed words
    return formatted_response

@app.route('/', methods=['GET', 'POST'])
def index():
    chatgpt_response = None

    if request.method == 'POST':
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            abort(400, 'No file part')

        filename = secure_filename(uploaded_file.filename)

        if filename:
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400, 'Invalid file extension')

            pdf_content = uploaded_file.read()

            # Get ChatGPT response based on the PDF content
            chatgpt_response = get_chatgpt_response(pdf_content)



            if request.method == 'POST':
                return jsonify({'chatgpt_response': chatgpt_response})

    return render_template('index.html', chatgpt_response=chatgpt_response)

if __name__ == "__main__":
    app.run(debug=True)
