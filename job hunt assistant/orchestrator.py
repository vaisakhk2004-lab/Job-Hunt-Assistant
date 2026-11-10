from crewai import Crew,Process
import json
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from usa_jobs_api import fetch_usajobs
from agents.resume_cl_agent import get_resume_cl_agent,create_resume_cl_task
from agents.messaging_agent import get_messaging_agent,create_messaging_task
def load_resume():
    with open(r'C:\Users\VYSHAK\Downloads\crew multi agent\job hunt assistant\data\sample_resume.txt','r',encoding='utf-8') as f:
        return f.read()
def run_pipeline():
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent=get_messaging_agent()

    jd_task = create_jd_analysis_task(jd_agent)
    resume_task = create_resume_cl_task(resume_agent,jd_task)
    message_task=create_messaging_task(messaging_agent, jd_task)

    return Crew(
        agents=[jd_agent, resume_agent,messaging_agent],
        tasks=[jd_task, resume_task,message_task],
        process=Process.sequential,
        max_rpm=3,
        verbose=True,
    )
keyword = "software engineer"   
if __name__=='__main__':
    resume=load_resume()
    jobs=fetch_usajobs(keyword)
    if not jobs:
        raise SystemExit("No matching jobs found. Try another keyword or location.")
    for job in jobs:
        crew=run_pipeline()
        result=crew.kickoff(inputs={'details':json.dumps(job),'resume_text':resume})

