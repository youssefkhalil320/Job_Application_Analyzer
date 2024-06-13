from fpdf import FPDF


def export_summary_to_pdf(candidate_details, filename="candidate_summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section, content in candidate_details.items():
        if section == "questions_and_answers":
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(200, 10, txt="Questions and Answers", ln=True)

            for idx, qa in enumerate(content):
                pdf.set_font("Arial", 'B', size=12)
                pdf.cell(200, 10, txt=f"Question {idx+1}:", ln=True)

                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=qa["question"])

                pdf.set_font("Arial", 'B', size=12)
                pdf.cell(200, 10, txt="Answer:", ln=True)

                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=qa["answer"])

                pdf.set_font("Arial", 'B', size=12)
                pdf.cell(200, 10, txt="Evaluation:", ln=True)

                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=qa["evaluation"])

        elif section == "score":
            # Add the final score
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(200, 10, txt="Final Score", ln=True)

            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=content)

        else:
            # Add section title
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(200, 10, txt=section.replace("_", " ").title(), ln=True)

            # Add section content
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=content)

    pdf.output(filename)
