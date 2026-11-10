import crewai
from crewai import Task,Agent,LLM

import os,dotenv
from dotenv import load_dotenv
env_path = '/usercode/job_hunt_assistant/utils/.env'
load_dotenv(dotenv_path=env_path)
gemini_api_key=os.getenv('GEMINI_API_KEY')

llm = LLM(
    model='gemini-3.1-flash-lite',
    google_api_key=gemini_api_key,
    temperature=0.2,max_retries=1
)
def get_messaging_agent():
    return Agent(max_iter=3,role='message writer',goal='to help job seekers in writing outreach messages',llm=llm,backstory='You write concise, polite LinkedIn and email messages for job seekers.You are specific, never generic, and never exaggerate.')
def create_messaging_task(agent,jd_task):
    return Task(agent=agent,description="""
        Write a brief, professional message expressing the candidate's interest
        in the job described in the job analysis you were given as context.

        Rules:
        1. Mention the job title and organisation.
        2. Highlight one or two strengths from the resume that match the job.
        3. Use only facts present in the resume. Do not invent experience.
        4. End with a polite request for a conversation or next step.
        5. Use [Recipient Name] as the greeting placeholder.
        """,
        expected_output="""
        One message of at most 150 words, suitable for LinkedIn or email.
        Start with a greeting and end with the candidate's name.
        Output only the message, with no title, notes or explanation.
        """,context=[jd_task])