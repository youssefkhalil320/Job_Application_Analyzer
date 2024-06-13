from modules.pdf_parser import get_full_resume_text
from modules.gemini_chat import gemini_chat, model
from modules.prompts import summary_prompts, test_prompts
from modules.export_report import export_summary_to_pdf
from collections import defaultdict
import time

num_questions_per_prompt = 2

chat = model.start_chat(history=[])

data = get_full_resume_text("./examples/Khalil_sResumeAPR2024.pdf")

questions_prompts_keys = ["years_of_experience_prompt",
                          "education_prompt", "job_titles_prompt", "skills_prompt"]

test_prompts_keys = ["Questions_according_to_jobs",
                     "Questions_related_to_skills"]

candidate_details = defaultdict(str)

response = chat.send_message(summary_prompts["description_prompt"])
time.sleep(15)
response = chat.send_message(data)
time.sleep(15)


def get_summary():
    for prompt in questions_prompts_keys:
        response = chat.send_message(summary_prompts[prompt]).text
        print(response)
        candidate_details[prompt] = response
        time.sleep(30)


def get_questions():
    score = 0
    total_questions = num_questions_per_prompt * len(test_prompts_keys)
    question_answers = []

    for prompt in test_prompts_keys:
        for i in range(num_questions_per_prompt):
            question = chat.send_message(test_prompts[prompt]).text
            print(question)
            answer = input("Write your answer please: ")
            evaluation = chat.send_message(answer).text
            print(evaluation)

            question_answers.append({
                "question": question,
                "answer": answer,
                "evaluation": evaluation
            })

            if "wrong" not in evaluation.lower():
                score += 1

            time.sleep(30)

    candidate_details["questions_and_answers"] = question_answers
    candidate_details["score"] = f"{score} out of {total_questions}"
    return score, total_questions


get_summary()
score, total_questions = get_questions()
print(f"Final Score: {score} out of {total_questions}")
export_summary_to_pdf(candidate_details, "./Reports/Khalil_details.pdf")
