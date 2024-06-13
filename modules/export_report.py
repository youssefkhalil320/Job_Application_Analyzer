from fpdf import FPDF


def export_summary_to_pdf(candidate_details, filename="candidate_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section, content in candidate_details.items():
        # Add section title
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt=section.replace("_", " ").title(), ln=True)

        # Add section content
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=content)

    pdf.output(filename)
