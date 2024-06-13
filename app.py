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
    resume_summary = ""
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


def get_questions(input_text, state):
    global candidate_details
    score = state.get("score", 0)
    question_index = state.get("question_index", 0)
    total_questions = num_questions_per_prompt * len(test_prompts_keys)
    question_answers = state.get("question_answers", [])

    # If it's the first interaction, ask the first question
    if question_index == 0:
        state["question_answers"] = []
        state["score"] = 0
        state["question_index"] = 0
        question = chat.send_message(test_prompts[test_prompts_keys[0]]).text
        state["current_question"] = question
        state["question_index"] += 1
        return [("Bot", question)], state

    # Process the user's answer to the previous question
    if "current_question" in state:
        question = state["current_question"]
        answer = input_text
        evaluation = chat.send_message(answer).text

        question_answers.append({
            "question": question,
            "answer": answer,
            "evaluation": evaluation
        })

        if "wrong" not in evaluation.lower():
            score += 1

        state["question_answers"] = question_answers
        state["score"] = score

        if question_index < total_questions:
            prompt_key = test_prompts_keys[question_index //
                                           num_questions_per_prompt]
            question = chat.send_message(test_prompts[prompt_key]).text
            state["current_question"] = question
            state["question_index"] += 1
            # Introduce a delay of 15 seconds before asking the next question
            time.sleep(15)
            return [("User", answer), ("Bot", evaluation), ("Bot", question)], state

    candidate_details["questions_and_answers"] = question_answers
    candidate_details["score"] = f"{score} out of {total_questions}"
    final_message = f"Final score: {candidate_details['score']}. Now you can download the report."
    return [("User", answer), ("Bot", evaluation), ("Bot", final_message)], state


def generate_report(name):
    global candidate_details
    file_path = f"./Reports/{name}_details.pdf"
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
        chat_state = gr.State({})

        send_button.click(fn=get_questions, inputs=[
                          message, chat_state], outputs=[chatbot, chat_state])
        message.submit(fn=get_questions, inputs=[
                       message, chat_state], outputs=[chatbot, chat_state])

    with gr.Tab("Generate Report"):
        name_input = gr.Textbox(label="Enter your name")
        generate_button = gr.Button("Generate Report")
        report_output = gr.File()

        generate_button.click(fn=generate_report,
                              inputs=name_input, outputs=report_output)

demo.launch()
