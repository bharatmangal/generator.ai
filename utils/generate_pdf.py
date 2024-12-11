import os
from fpdf import FPDF

def generate_qa_pdf(content):
    # Ensure the static directory exists
    os.makedirs("./static", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # Add DejaVuSans font for Unicode support
    font_path_regular = os.path.join(os.getcwd(), "static/DejaVuSans.ttf")
    font_path_bold = os.path.join(os.getcwd(), "static/DejaVuSans-Bold.ttf")

    pdf.add_font("DejaVu", "", font_path_regular, uni=True)
    pdf.add_font("DejaVu-Bold", "", font_path_bold, uni=True)


    # Set font and add content
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, txt="Generated Assignment", ln=True, align='C')
    pdf.ln(10)  # Add space

    # Write the content directly to the PDF
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, txt=content.strip())

    # Save PDF
    output_file = "./static/generated_assignment.pdf"
    pdf.output(output_file)
    return output_file
