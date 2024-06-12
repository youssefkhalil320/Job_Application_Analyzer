from modules.pdf_parser import get_full_resume_text
from modules.gemini_chat import gemini_chat, model
from modules.prompts import summary_prompts
from modules.export_report import export_summary_to_pdf
from collections import defaultdict
import time

chat = model.start_chat(history=[])

data = get_full_resume_text("./examples/Khalil_sResumeAPR2024.pdf")

target_prompts = ["years_of_experience_prompt",
                  "education_prompt", "job_titles_prompt", "skills_prompt"]

candidate_details = defaultdict(str)

response = chat.send_message(summary_prompts["description_prompt"])
response = chat.send_message(data)


def get_summary(data):
    for prompt in target_prompts:
        response = chat.send_message(summary_prompts[prompt]).text
        print(response)
        candidate_details[prompt] = response
        time.sleep(30)

    return candidate_details


def get_questions(data):
    pass


candidate_details_dict = get_summary(data)
export_summary_to_pdf(candidate_details_dict, "./Reports/Khalil_details.pdf")
