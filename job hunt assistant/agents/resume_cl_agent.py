import os,dotenv
from dotenv import load_dotenv
from crewai import Task,Agent,LLM
from agents.jd_analyst import create_jd_analysis_task
env_path = r'C:\Users\VYSHAK\Downloads\Multi job assistant using Crew ai\job hunt assistant\.env'
load_dotenv(dotenv_path=env_path)
gemini_api_key=os.getenv('GEMINI_API_KEY')
llm = LLM(
    model='gemini-3.1-flash-lite',
    google_api_key=gemini_api_key,
    temperature=0.2,max_retries=1)

def get_resume_cl_agent():
    return Agent(max_iter=3,role='resume and cover letter maker',goal='to help job seekers tailor their resumes and cover letters',llm=llm,backstory='you are an expert at tailoring resume and writing cover letter based on the job requirements')

def create_resume_cl_task(agent,jd_task):
    return Task(agent=agent,output_file='/data/resume_agent_output.txt',description="""
Using the job analysis from the previous task and the candidate's master resume below,
create a tailored one-page resume and a cover letter.

Master resume:
{resume_text}

Rules:
1. Use ONLY facts present in the master resume. Never invent skills, tools, employers,
   dates, years of experience, citizenship, work authorization or location.
2. Keep the candidate's name and contact details exactly as in the master resume.
   If a detail is missing, omit it. Never write placeholders like [Your Name].
3. The master resume has more than fits on one page. Select only the projects, skills
   and bullets most relevant to this job and leave the rest out. Put the most relevant
   items first.
4. Use the job's keywords only where they truthfully describe the candidate's work.
5. If the job requires something the resume does not show, do not claim it.
""",
        expected_output="""
Exactly two sections, each starting with its marker on its own line:
<<RESUME>>
(the full tailored resume in plain text: based on the master resume provided.Tailor the resume to the job description, including only relevant 
skills, projects, experience ,education, certifications if present; fits one page)
<<COVER_LETTER>>
(a complete cover letter of about 250 words, signed with the candidate's name from the resume)
Output nothing before the first marker.
""",context=[jd_task])