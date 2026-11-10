import json, os
import streamlit as st
from usa_jobs_api import fetch_usajobs
from orchestrator import run_pipeline
OUTPUT = r'C:\Users\VYSHAK\Downloads\crew multi agent\job hunt assistant\data\resume_agent_output.txt'  

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
        with st.spinner('Searching USAJOBS...'):
            jobs = fetch_usajobs(keyword.strip(), location=location.strip() or 'remote',
                                 results_per_page=50, limit=5)
        st.session_state.jobs = jobs
        st.session_state.resume_text = resume_text
        st.session_state.pop('result', None)


if 'jobs' in st.session_state:
    jobs = st.session_state.jobs
    if not jobs:
        st.warning('No matching jobs found. Try another keyword or location.')
    else:
        labels = [f"{j['title']} - {j['organization']} ({j['location']})" for j in jobs]
        choice = st.selectbox('Select a job', range(len(jobs)), format_func=lambda i: labels[i])
        job = jobs[choice]

        with st.expander('Job details'):
            st.write(job['duties'])
            st.write(job['qualifications'])
            st.caption(job['url'])

        if st.button('Generate application'):
            if os.path.exists(OUTPUT):
                os.remove(OUTPUT)
            try:
                with st.spinner('Running the agents (this takes a few minutes)...'):
                    crew = run_pipeline()
                    result = crew.kickoff(inputs={
                        'details': json.dumps(job, indent=2),
                        'resume_text': st.session_state.resume_text,
                    })
                st.session_state.result = str(result)
                st.session_state.resume_output = (
                    open(OUTPUT, encoding='utf-8').read() if os.path.exists(OUTPUT) else ''
                )
            except Exception as e:
                st.error(f'The pipeline failed: {e}')


if 'result' in st.session_state:
    st.markdown('### Outreach message')
    st.write(st.session_state.result)
    if st.session_state.get('resume_output'):
        st.markdown('### Tailored resume and cover letter')
        st.text(st.session_state.resume_output)