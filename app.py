from dotenv import load_dotenv

load_dotenv()
 
import base64 
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content(input,pdf_content,prompt)
    return response.text

def convert_pdf_to_image(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type" : "image.jpeg",
                "data" : base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
## Streamlit APP

st.set_page_config(page_title="Gemini ATS: Intelligent Resume Screening")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description:", key="input")
uploaded_file=st.file_uploader("Upload your Resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

# submit3 = st.button("What are the Keyowords That are Missing")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

# input_prompt2 = """
# You are an experienced Technical Human Resource Manager,your task is to scrutinize the resume 
# in light of the job desciption provided.Share your insights on the candidate's suitability for 
# the role from an HR perspective.
# Additionally, offer advice on enhancing the candidate's skills and identify areas that are lacking
# """

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, Full stack web development,
Big Data Engineer, DEVops, Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=convert_pdf_to_image(uploaded_file)
        responcse=get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("The Response is")
        st.write(responcse)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=convert_pdf_to_image(uploaded_file)
        responcse=get_gemini_response(input_text,pdf_content,input_prompt3)
        st.subheader("The Response is")
        st.write(responcse)
    else:
        st.write("Please upload the resume")