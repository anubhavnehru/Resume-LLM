import streamlit as st
import openai
from openai import OpenAI
import os
import PyPDF2 as pdf
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Set your OpenAI API key



api_key = os.getenv("GPT_API_KEY")

client = OpenAI(api_key= api_key,)

# Prompt Template
input_prompt = """
Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving their resumes. Classify the job title for the candidate based on the resume and provide 
a match percentage based on the Job description and the missing keywords with high accuracy.
However, for the purpose of this task, only return the classified job title without the match percentage.
resume:{text}
description:{jd}

Ensure the missing keywords are technical skills, assuming what a hiring manager will be looking in my resume
I want the response in paragraph having the structure :

Classified Job Title : "%"

JD Match :"%"

Missing Keywords : "

Recommendations :""

"""

def get_chatgpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a skilled HR professional with a strong 10+ years experience of extracting information from resumes 
             and matching resumes with job descriptions. Your job is to return accurate job title for the resume, percentage mathcing of job description with the resume and return a list of missing keywords """},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.1
    )
    # Assuming the response content is directly accessible
    return response.choices[0].message.content.strip()

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "  # Adding a space for better readability
    return text

def display_response_sections(response):
    # Display each section of the response in separate markdowns
    sections = response.split("\n\n")
    for section in sections:
        st.markdown(f"**{section.split(':')[0]}**")
        st.markdown(section.split(':')[1])

# Streamlit app UI
st.title("Smart Resume Job Category ATS LLM")
st.text("Improve Your Resume ATS score")
jd = st.text_area("Please Paste the Job Description")
uploaded_file = st.file_uploader("Please Upload Your Resume", type="pdf", help="Please upload the PDF")

if st.button("Submit"):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=text, jd=jd)
        response = get_chatgpt_response(prompt)
        display_response_sections(response)
