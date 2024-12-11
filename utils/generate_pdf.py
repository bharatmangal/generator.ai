import os
from fpdf import FPDF
import time

def generate_qa_pdf(content):
    # Ensure the static directory exists (if needed for other uses)
    static_path = "./static"
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    # Create a temporary file in /tmp
    output_file = f"/tmp/generated_assignment_{time.time()}.pdf"

    # Create PDF instance
    pdf = FPDF()
    pdf.add_page()

    # Add fonts to PDF
    pdf.add_font("DejaVu", "", "static/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu-Bold", "", "static/DejaVuSans-Bold.ttf", uni=True)

    # Set font and add content
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, txt="Generated Assignment", ln=True, align='C')
    pdf.ln(10)  # Add space

    # Write the content directly to the PDF
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, txt=content.strip())

    # Save PDF in temporary file location
    try:
        pdf.output(output_file)
    except IOError as e:
        raise IOError(f"Failed to write PDF: {str(e)}")

    return output_file
