import os 
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")

if not api_key:
    raise ValueError("API KEY IS NOT CONFIGURED")

client = genai.Client(api_key=api_key)

generation_config={
    'max_output_tokens' : 1000,
    'thinking_level' : 'medium',
}
student_name= input("Student name:")
education = input("Education: ")
skills = input("Your current technical skills (comma sperated): ")
projects = input("Projects (Comma seperated): ")
experience = input("Experinece / Internship if any : ")
target_role = input("Target job roles:")

user_input =  input("Enter your query: ")

student_context = f"""
STUDENT PROFILE

Name:{student_name}
Education:{education}
Techincal skills:{skills}
Projects:{projects}
Experience/Internship:{experience}
Target Role:{target_role}
"""


career_prompt= f""""
ROLE:
You are CareerTwin, You are an AI career advisor for post-grad students

OBJECTIVE:
Analyze the students current profile against their target job role

CONTEXT:
CareerTwin helps students understand software engineering career paths, required technical skills,learning priorities,projectsand interview preparation 

TASK:
Answer the student's career related question clearly and practically. Give recommnedations that are relevant to the students career goal

CONSTRAINTS:
- Do not provide unrelated information
- Do not assume skills that the stduent has not mentioned
- Prefer practical and actionable recommendations
- Keep the response concise and easy to understand

{student_context}
STUDENT QUESTION:
{user_input}

""" 

response = client.interactions.create(
    model = gemini_model,
    input = career_prompt,
    generation_config=generation_config,
)
print("****GEMINI****")
print(response.output_text)