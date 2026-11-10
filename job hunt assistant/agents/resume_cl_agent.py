import os,dotenv
from dotenv import load_dotenv
from crewai import Task,Agent,LLM
from agents.jd_analyst import create_jd_analysis_task
env_path = '/usercode/job_hunt_assistant/utils/.env'
load_dotenv(dotenv_path=env_path)
gemini_api_key=os.getenv('GEMINI_API_KEY')
llm = LLM(
    model='gemini-3.1-flash-lite',
    google_api_key=gemini_api_key,
    temperature=0.2,max_retries=1)

def get_resume_cl_agent():
    return Agent(max_iter=3,role='resume and cover letter maker',goal='to help job seekers tailor their resumes and cover letters',llm=llm,backstory='you are an expert at tailoring resume and writing cover letter based on the job requirements')

def create_resume_cl_task(agent,jd_task):
    return Task(agent=agent,output_file='/data/resume_agent_output.txt',description="""tailor resumes and generate personalized cover letters professionally based on a job description.The resume text is a master resume containing more than will fit on one page.
Choose only the projects, skills and bullets most relevant to this job and leave the rest out.
Two different jobs should produce visibly different resumes. you will  be provided with a resume_text{resume_text}. Do not invent skills or experience.""",
    expected_output="""
        Exactly two sections, each starting with its marker on its own line:
        <<RESUME_SUMMARY>>
        (a tailored resume summary of 3-4 sentences)
        <<COVER_LETTER>>
        (a complete cover letter, about 250 words)
        Output nothing before the first marker.
        """,context=[jd_task])