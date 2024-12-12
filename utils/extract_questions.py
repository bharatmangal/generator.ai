from PyPDF2 import PdfReader

def extract_questions(pdf_file):
    reader = PdfReader(pdf_file)
    questions = ""
    for page in reader.pages:
        questions += page.extract_text() + "\n"
    return questions
    print(questions)