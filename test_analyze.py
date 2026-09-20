import requests
import json

url = "http://127.0.0.1:8000/api/orchestrator/analyze"

with open("dummy.txt", "w") as f:
    f.write("Dummy resume text")

files = {'resume_file': open('dummy.txt', 'rb')}
data = {'job_description': 'Software Engineer'}

response = requests.post(url, files=files, data=data)
print(response.status_code)
print(response.text)
