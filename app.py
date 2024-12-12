from flask import Flask, request, send_file, render_template
from utils.extract_questions import extract_questions
from utils.generate_answers import generate_answers
from utils.generate_pdf import generate_qa_pdf
from utils.handwriting import convert_to_handwriting
from utils.compress_pdf import compress_pdf
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Frontend form for uploads

@app.route("/process", methods=["POST"])
def process():
    # Step 1: Upload and extract questions
    file = request.files["file"]
    input_pdf_path = os.path.join('/tmp', file.filename)
    file.save(input_pdf_path)

    # Step 2: Extract questions
    questions = extract_questions(input_pdf_path)

    # Step 3: Generate answers
    answers = generate_answers(questions)

    # Step 4: Generate structured Q&A PDF
    qa_pdf = generate_qa_pdf(answers)

    # Step 5: Convert to handwriting
    handwriting_pdf = convert_to_handwriting(qa_pdf)

    # Step 6: Compress PDF
    compressed_pdf_path = compress_pdf(handwriting_pdf)

    # Provide the download link for the compressed PDF
    return render_template(
        "download.html",
        qa_pdf_path=qa_pdf,
        handwriting_pdf_path=handwriting_pdf,
        compressed_pdf_path=compressed_pdf_path
    )

@app.route("/download")
def download():
    # Serve all three PDFs
    qa_pdf_path = request.args.get('qa_pdf_path')
    handwriting_pdf_path = request.args.get('handwriting_pdf_path')
    compressed_pdf_path = request.args.get('compressed_pdf_path')

    if qa_pdf_path and os.path.exists(qa_pdf_path) and \
       handwriting_pdf_path and os.path.exists(handwriting_pdf_path) and \
       compressed_pdf_path and os.path.exists(compressed_pdf_path):
        
        return render_template(
            "download.html",
            qa_pdf_path=qa_pdf_path,
            handwriting_pdf_path=handwriting_pdf_path,
            compressed_pdf_path=compressed_pdf_path
        )
    else:
        return "One or more files not found", 404

if __name__ == "__main__":
    app.run(debug=True)
