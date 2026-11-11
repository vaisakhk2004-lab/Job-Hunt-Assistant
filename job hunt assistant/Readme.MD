# Job Hunt Assistant
App Link:-https://job-hunt-assistant-dgxnfrjpqpcb5qlkyefpgf.streamlit.app
A multi-agent application that takes a job keyword and your resume, finds matching listings from the USAJOBS API, and generates a tailored resume summary, cover letter and outreach message for the job you pick.

Built with [CrewAI](https://www.crewai.com/), Google Gemini, Streamlit and the USAJOBS Search API.

## How it works

1. **Search**: `usa_jobs_api.py` queries the USAJOBS Search API by keyword and location, filters results by title, and returns the position title, organization, location, qualifications, duties and URL.
2. **Select**: the Streamlit app lists the matches. You pick one and review its details.
3. **Generate**: a sequential CrewAI pipeline of three agents runs on the selected job and your resume:
   - **JD Analyst**: extracts the job title, company, location, required skills, experience, education and key responsibilities into a structured Markdown report.
   - **Resume and Cover Letter Agent**: reads your master resume, picks the projects, skills and bullets most relevant to the role, and writes a 3-4 sentence tailored resume summary and a cover letter of about 250 words.
   - **Messaging Agent**: writes an outreach message of at most 150 words for LinkedIn or email, using only facts from your resume.
4. **Review**: the app shows the outreach message, and the resume summary and cover letter saved to `data/resume_agent_output.txt`.

```
Keyword + Location + Resume
        │
        ▼
 USAJOBS API  ──►  Job list  ──►  Selected job
                                      │
                                      ▼
                          JD Analyst (report.md)
                           │                  │
                           ▼                  ▼
          Resume & Cover Letter Agent    Messaging Agent
                           │                  │
                           ▼                  ▼
            Resume summary + cover letter   Outreach message
```

All agents run on Gemini through CrewAI's `LLM` class at temperature 0.2. The prompts forbid inventing skills or experience, and the crew is rate-limited to 3 requests per minute.

## Project structure

```
job hunt assistant/
├── agents/
│   ├── jd_analyst.py          # JD analysis agent and task
│   ├── resume_cl_agent.py     # Resume summary and cover letter agent and task
│   └── messaging_agent.py     # Outreach message agent and task
├── data/
│   ├── sample_resume.txt      # Resume used by the CLI runner
│   ├── report.md              # JD analysis output
│   └── resume_agent_output.txt# Generated resume summary and cover letter
├── orchestrator.py            # Builds the CrewAI crew; CLI runner
├── streamlit_app.py           # Web interface
├── usa_jobs_api.py            # USAJOBS API client
└── .env                       # API keys (not committed)
```

## Setup

**Requirements:** Python 3.10+

```bash
pip install crewai streamlit requests python-dotenv
```

Create a `.env` file in the project root:

```
USAJOBS_API_KEY=your_usajobs_key
GEMINI_API_KEY=your_gemini_key
```

Get a free USAJOBS API key at <https://developer.usajobs.gov/> and a Gemini key from [Google AI Studio](https://aistudio.google.com/).

Update the file paths in `usa_jobs_api.py`, `orchestrator.py`, `streamlit_app.py` and the three agent files to match your machine, and set the `User-Agent` header in `usa_jobs_api.py` to the email you registered with USAJOBS. Run the app from the project folder so the `data/` output paths resolve correctly.

## Usage

**Web app**

```bash
streamlit run streamlit_app.py
```

Enter a job keyword, a location (default `remote`) and your resume text, then click **Find jobs**. Select a listing and click **Generate application**. A run takes a few minutes because of the rate limit.

**Command line**

```bash
python orchestrator.py
```

Searches for the keyword set in `orchestrator.py`, then runs the full pipeline on each matching job using `data/sample_resume.txt`.

## Limitations

- USAJOBS lists US federal positions only, and many require US citizenship.
- Output quality depends on the resume text you provide and on the LLM. Always review the generated documents before sending them.

## Tech stack

Python, CrewAI, Google Gemini, Streamlit, Requests, python-dotenv, USAJOBS REST API
