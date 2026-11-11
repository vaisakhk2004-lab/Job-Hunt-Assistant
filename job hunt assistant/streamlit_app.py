import json, os
from pathlib import Path
import streamlit as st

BASE = Path(__file__).parent
os.chdir(BASE)  # agents write to relative data/ paths, so run from this folder
(BASE / "data").mkdir(exist_ok=True)

# Cloud: copy Streamlit secrets into the environment before the agent modules read them
try:
    for k in ("USAJOBS_API_KEY", "USAJOBS_EMAIL", "GEMINI_API_KEY"):
        if k in st.secrets:
            os.environ[k] = st.secrets[k]
except Exception:
    pass  # local run: keys come from .env

from usa_jobs_api import fetch_usajobs
from orchestrator import run_pipeline

st.title('Job assistant')

with st.form('search_form'):
    keyword = st.text_input('Job keyword', placeholder='e.g. data scientist')
    location = st.text_input('Location', value='remote')
    resume_text = st.text_area('Resume text', height=300)
    searched = st.form_submit_button('Find jobs')

if searched:
    if not keyword.strip() or not resume_text.strip():
        st.warning('Please enter a job keyword and your resume text.')
    else:
        try:
            with st.spinner('Searching USAJOBS...'):
                jobs = fetch_usajobs(keyword.strip(), location=location.strip() or 'remote',
                                     results_per_page=50, limit=5)
            st.session_state.jobs = jobs
            st.session_state.resume_text = resume_text
            st.session_state.pop('result', None)
            st.session_state.pop('resume_output', None)
        except Exception as e:
            st.error(f'Job search failed: {e}')

if 'jobs' in st.session_state:
    jobs = st.session_state.jobs
    if not jobs:
        st.warning('No matching jobs found. Try another keyword or location.')
    else:
        labels = [f"{j['title']} - {j['organization']} ({j['location']})" for j in jobs]
        choice = st.selectbox('Select a job', range(len(jobs)), format_func=lambda i: labels[i])
        job = jobs[choice]
        if st.button('Generate application'):
            try:
                with st.spinner('Running the agents (this takes a few minutes)...'):
                    crew = run_pipeline()
                    result = crew.kickoff(inputs={
                        'details': json.dumps(job, indent=2),
                        'resume_text': st.session_state.resume_text,
                    })
                # Tasks run in order: JD analysis, resume + cover letter, outreach message
                st.session_state.jd_report = result.tasks_output[0].raw
                st.session_state.resume_output = result.tasks_output[1].raw
                st.session_state.result = result.tasks_output[2].raw
            except Exception as e:
                st.error(f'The pipeline failed: {e}')

if 'result' in st.session_state:
    st.markdown('### Job description')
    st.text(st.session_state.jd_report)
    st.markdown('### Outreach message')
    st.write(st.session_state.result)
    if st.session_state.get('resume_output'):
        st.markdown('### Tailored resume and cover letter')
        st.text(st.session_state.resume_output)