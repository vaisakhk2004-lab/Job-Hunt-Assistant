import requests,os
from dotenv import load_dotenv
env_path = r'C:\Users\VYSHAK\Downloads\Multi job assistant using Crew ai\job hunt assistant\.env'
load_dotenv(env_path)
job_api_key=os.getenv('USAJOBS_API_KEY')
if not job_api_key :
    raise RuntimeError("Set USAJOBS_API_KEY and USAJOBS_EMAIL in .env")
def fetch_usajobs(keyword, location="remote",results_per_page=5,limit=3):
    headers={'Host':"data.usajobs.gov",
            'User-Agent':'vaisakhk077@gmail.com',
            'Authorization-Key': job_api_key}
    params={'Keyword':keyword,'LocationName':location,
            'ResultsPerPage':results_per_page}
    BASE_URL='https://data.usajobs.gov/api/Search'
    response=requests.get(BASE_URL,params=params,headers=headers)
    response.raise_for_status()
    jobs=response.json()
    if not jobs:
        return "No jobs found."
    results=jobs['SearchResult']['SearchResultItems']
    jobs = []
    words=keyword.lower()
    for i in results:
        d = i['MatchedObjectDescriptor']
        title = d.get('PositionTitle', '').lower()
        if any(w in title for w in words):
            jobs.append({
                "title": d.get('PositionTitle'),
                "organization": d.get('OrganizationName'),
                "location": d.get('PositionLocationDisplay'),
                "qualifications": d.get('QualificationSummary'),
                "duties": d.get('UserArea', {}).get('Details', {}).get('JobSummary'),
                "url": d.get('PositionURI'),
            })
    return jobs[:limit]
    
    

#     print("Status code:", response.status_code)
    
print(job_api_key)



    
    

    
# fetch_usajobs(keyword="business analyst")

