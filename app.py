import gradio as gr
from modules.pdf_parser import get_full_resume_text
from modules.gemini_chat import gemini_chat, model
from modules.prompts import summary_prompts, test_prompts
from modules.export_report import export_summary_to_pdf
from collections import defaultdict
import time

num_questions_per_prompt = 2

chat = model.start_chat(history=[])

questions_prompts_keys = ["years_of_experience_prompt",
                          "education_prompt", "job_titles_prompt", "skills_prompt"]

test_prompts_keys = ["Questions_according_to_jobs",
                     "Questions_related_to_skills"]

candidate_details = defaultdict(str)


def analyze_resume(file):
    global candidate_details
    resume_summary = """
"""
    data = get_full_resume_text(file.name)
    candidate_details = defaultdict(str)

    response = chat.send_message(summary_prompts["description_prompt"]).text
    time.sleep(15)
    response = chat.send_message(data).text
    time.sleep(15)

    for prompt in questions_prompts_keys:
        response = chat.send_message(summary_prompts[prompt]).text
        resume_summary += f"{response} \n"
        candidate_details[prompt] = response
        time.sleep(30)

    return resume_summary


def interactive_chat(input_text, state):
    if not state:
        response = "Hi, welcome to the interview. Let's get started with the questions."
        state.append(("Bot", response))
        return state, state

    last_entry = state[-1]
    if last_entry[0] == "Bot" and "Let's get started" in last_entry[1]:
        score, total_questions = get_questions(state)
        final_message = f"Final score: {score} out of {total_questions}. Now you can download the report."
        state.append(("Bot", final_message))
        return state, state

    response = chat.send_message(input_text).text
    state.append((input_text, response))
    return state, state


def get_questions(state):
    global candidate_details
    score = 0
    total_questions = num_questions_per_prompt * len(test_prompts_keys)
    question_answers = []

    for prompt in test_prompts_keys:
        for i in range(num_questions_per_prompt):
            question = chat.send_message(test_prompts[prompt]).text
            state.append(("Bot", question))

            # Wait for user response
            while len(state) <= (i + 1) * 2:
                time.sleep(1)

            answer = state[-1][1]
            evaluation = chat.send_message(answer).text

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


def generate_report():
    global candidate_details
    file_path = "./Reports/Khalil_details.pdf"
    export_summary_to_pdf(candidate_details, file_path)
    return file_path


# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Candidate Report Generator")

    with gr.Tab("Analyze Resume"):
        with gr.Column():
            resume_file = gr.File(label="Upload Resume")
            analyze_button = gr.Button("Analyze")
            analyze_output = gr.Textbox()

            analyze_button.click(
                fn=analyze_resume, inputs=resume_file, outputs=analyze_output)

    with gr.Tab("Virtual Interview"):
        chatbot = gr.Chatbot()
        message = gr.Textbox(label="Enter your message")
        send_button = gr.Button("Send")
        chat_state = gr.State([])

        send_button.click(fn=interactive_chat, inputs=[
                          message, chat_state], outputs=[chatbot, chat_state])
        message.submit(fn=interactive_chat, inputs=[
                       message, chat_state], outputs=[chatbot, chat_state])

    with gr.Tab("Generate Report"):
        generate_button = gr.Button("Generate Report")
        report_output = gr.File()

        generate_button.click(fn=generate_report,
                              inputs=[], outputs=report_output)

demo.launch()
