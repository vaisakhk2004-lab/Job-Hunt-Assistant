
from crewai import Task,Agent,LLM
import os
from dotenv import load_dotenv
env_path = 'C:\\Users\\VYSHAK\\Downloads\\crew multi agent\\.env'
load_dotenv(dotenv_path=env_path)
gemini_api_key=os.getenv('GEMINI_API_KEY')

llm = LLM(
    model='gemini-3.1-flash-lite',
    google_api_key=gemini_api_key,
    temperature=0.2,max_retries=1
)
def get_jd_analyst_agent():
    return Agent(role='Job description analyser',goal=f'to analyse the job descriptions in a professional way based on the details provided',backstory='you are an expert at analysing the job description and summarizing it',llm=llm,allow_delegation=False)

def create_jd_analysis_task(agent):
    return Task(agent=agent,output_file='/data/report.md',description="""
        Analyse the provided job description {details} and extract:
        1. Job title
        2. Company name
        3. Job location
        4. Required technical skills
        5. Required experience
        6. Educational qualifications
        7. Key responsibilities
        """,
        expected_output="""
        A structured Markdown report containing all the extracted
        job details, organised under appropriate headings.
        """)