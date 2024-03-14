# Resume Review Assistant

This Flask application serves as a tool for refining resumes by leveraging OpenAI's ChatGPT model. It allows users to upload PDF resumes and receive detailed feedback on various aspects such as clarity, relevance, impact, professionalism, grammar, and language.

## Prerequisites

Before running this application, make sure you have the following:

- Python 3.x installed on your system.
- `pip` package manager installed.
- OpenAI API key. If you don't have one, sign up at [OpenAI](https://openai.com) and obtain your API key.

## Installation

1. Clone or download this repository to your local machine.
2. Navigate to the project directory.

```
cd resume-review-assistant
```

3. Install dependencies using pip.

```
pip install -r requirements.txt
```

4. Set up your environment variables:

    - Create a `.env` file in the root directory.
    - Add your OpenAI API key to the `.env` file:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. Run the Flask application:

```
python app.py
```

2. Access the application in your web browser at `http://127.0.0.1:5000/`.

3. Upload your resume in PDF format.
4. Enter your Job profile

5. Click the submit button to initiate the review process.

6. The application will use ChatGPT to analyze your resume and provide feedback based on various metrics.

## Files

- `app.py`: Flask application code for the backend.
- `templates/index.html`: HTML file for the frontend user interface.

## Credits

This application was developed by Omair Ansari.
