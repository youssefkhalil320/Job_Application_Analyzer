summary_prompts = {
    "description_prompt": """
    - I am a recruiter and you are a virtual assistant
    - I will provide you with candidate resumes and ask you questions about them
    - If I ask you about experience summary please show the years of experience and the companies he worked for. Just mention the Job title and the company Name.
    - If I ask you about education summary please show the years of education and the schools he graduated from
    - If I ask you about skills summary please show the skills he has
    - If I ask you about projects summary please show the projects he has worked on. Just give the headlines of the projects.
    - If I ask you about interests summary please show the interests he has
    Do not provide any summary or Information until I ask you for specific information.
    """,
    "years_of_experience_prompt": """
    How many years of experience does the candidate have?
    - Please include Internships, training, part-time and full-time jobs
    """,
    "education_prompt": """
    What kind of education did the candidate have?
    Please include Bachelor degree, Post-graduate degrees (Master, PhD and post-doc) and Diplomas
    """,
    "job_titles_prompt": """
    Please provide the job titles and companies
    - Example: Junior software engineer@Google
    """,
    "skills_prompt": """
    Please provide the skills the candidate has
    - Example: Python, Java, C++, HTML
    """
}

test_prompts = {
    "Questions_according_to_jobs": """
- You will to a virtual chat interview for the candidate 
- Please generate MCQ question about one of the topics the candidate worked on through his professional experience
- wait for the candidate to answer the question if the answer is correct return "correct" if it is wrong return "wrong"
""",
    "Questions_related to_skills": """
- You will to a virtual chat interview for the candidate 
- Please generate MCQ question about one of the skills the candidate wrote in his resume
- wait for the candidate to answer the question if the answer is correct return "correct" if it is wrong return "wrong"
"""
}
