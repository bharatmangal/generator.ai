from flask import Flask, request, send_file, render_template
from utils.extract_questions import extract_questions
from utils.generate_answers import generate_answers
from utils.generate_pdf import generate_qa_pdf
from utils.handwriting import convert_to_handwriting
from utils.compress_pdf import compress_pdf

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Frontend form for uploads

@app.route("/process", methods=["POST"])
def process():
    # Step 1: Upload and extract questions
    file = request.files["file"]
    questions = extract_questions(file)

    # Step 2: Generate answers
    answers = generate_answers(questions)

    # Step 3: Generate structured Q&A PDF
    qa_pdf = generate_qa_pdf(answers)

    # Step 4: Convert to handwriting
    handwriting_pdf = convert_to_handwriting(answers)

    # Step 5: Compress PDF
    compressed_pdf = compress_pdf(handwriting_pdf)

    # Return the generated PDFs
    return render_template(
        "download.html",
    )

if __name__ == "__main__":
    app.run(debug=True)
