import os
import gradio as gr
from pdfminer.high_level import extract_text
from docx import Document
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize Groq client with your API key
key = os.getenv("GroqCV")
client = Groq(api_key=key)

# Function to read PDF files
def read_pdf(file_path):
    text = extract_text(file_path)
    return text

# Function to read DOCX files
def read_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to analyze CV for role fit using Llama 3.3 and Groq API
def analyze_cv_with_llama(cv_text, job_description):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a hiring expert with extensive experience in talent acquisition. "
                    "Analyze the following CV content against a job description and score over 100 in these areas: "
                    "Relevance to the job, Work experience, Skills, Educational background, Achievements and Impact, "
                    "and Format and Presentation. Provide detailed scores and feedback for each area, make sure you put the name of the candidate bold as heading."
                )
            },
            {"role": "user", "content": f"Job Description:\n{job_description}\n\nCV:\n{cv_text}"}
        ],
        temperature=0.7,
        max_tokens=2048,
        top_p=0.9,
        stream=False,
        stop=None,
    )
    # Collect and return the analysis response
    analysis_text = ''.join([chunk.message.content for chunk in completion.choices])
    return analysis_text

# Function to generate a PDF with analysis results
def generate_pdf(content, output_path):
    pdf = canvas.Canvas(output_path, pagesize=letter)
    pdf.setFont("Helvetica", 10)
    width, height = letter
    y = height - 40  # Start position
    
    for line in content.split("\n"):
        pdf.drawString(40, y, line)
        y -= 15  # Move down for the next line
        if y < 40:  # Create a new page if space is insufficient
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 40
    
    pdf.save()

# Function to handle file upload and job screening
def process_file(file, job_description):
    # Save the uploaded file to a temporary location
    file_path = file.name
    file_extension = os.path.splitext(file_path)[1].lower()

    # Read the file content based on its format
    if file_extension == ".pdf":
        cv_text = read_pdf(file_path)
    elif file_extension == ".docx":
        cv_text = read_docx(file_path)
    else:
        return "Unsupported file format", None

    # Analyze the CV against the job description
    analysis_result = analyze_cv_with_llama(cv_text, job_description)

    # Generate PDF with analysis results
    output_pdf_path = "cv_analysis_result.pdf"
    generate_pdf(analysis_result, output_pdf_path)

    return analysis_result, output_pdf_path

# Gradio Interface
def main():
    with gr.Blocks() as iface:
        with gr.Row():
            file_input = gr.File(label="Upload CV/Resume (PDF or DOCX)")
            job_description_input = gr.Textbox(label="Enter Job Description", lines=5, placeholder="Type the job description here...")

        analysis_output = gr.Markdown(label="CV Screening Analysis")
        download_button = gr.File(label="Download Analysis as PDF")
        
        def process_input(file, job_description):
            if not file or not job_description.strip():
                return "Please upload a file and provide a job description.", None
            return process_file(file, job_description)
        
        submit_button = gr.Button("Analyze CV")
        submit_button.click(process_input, [file_input, job_description_input], [analysis_output, download_button])

    iface.launch(share=True)

if __name__ == "__main__":
    main()
