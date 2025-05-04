import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import PyPDF2
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
from pathlib import Path

class ResumeMatchAnalyzer:
    def __init__(self):
        # Download all necessary NLTK data
        try:
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            nltk.download('maxent_ne_chunker')
            nltk.download('words')
        except Exception as e:
            print(f"Error downloading NLTK data: {e}")
        
        # Define regex patterns
        self.float_regex = re.compile(r'^\d{1,2}(\.\d{1,2})?$')
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.float_digit_regex = re.compile(r'^\d{10}$')
        self.email_with_phone_regex = re.compile(r'(\d{10}).|.(\d{10})')
        
        # Load NLP model with all required components
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["ner"])
            # Add the required components explicitly
            self.nlp.add_pipe("tagger")
            self.nlp.add_pipe("attribute_ruler")
        except OSError:
            print("Downloading spaCy model...")
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm", disable=["ner"])
            self.nlp.add_pipe("tagger")
            self.nlp.add_pipe("attribute_ruler")

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file."""
        try:
            # Convert string path to Path object and resolve it
            pdf_path = Path(pdf_path).resolve()
            
            if not pdf_path.exists():
                print(f"PDF file not found: {pdf_path}")
                return ""
                
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {str(e)}")
            return ""

    def tokenize_text(self, text):
        """Tokenize text using spaCy."""
        doc = self.nlp(text, disable=["tagger", "parser"])
        tokens = [(token.text.lower(), token.label_) for token in doc.ents]
        return tokens

    def extract_cgpa(self, resume_text):
        """Extract CGPA from resume text."""
        cgpa_pattern = r'\b(?:CGPA|GPA|C\.G\.PA|Cumulative GPA)\s*:?[\s-]([0-9]+(?:\.[0-9]+)?)\b|\b([0-9]+(?:\.[0-9]+)?)\s(?:CGPA|GPA)\b'
        match = re.search(cgpa_pattern, resume_text, re.IGNORECASE)
        if match:
            cgpa = match.group(1) if match.group(1) else match.group(2)
            return float(cgpa)
        return None

    def analyze_resumes(self, resumes_folder, job_desc_path, skills_keywords=None):
        """Analyze resumes against a job description."""
        try:
            # Convert paths to Path objects and resolve them
            resumes_folder = Path(resumes_folder).resolve()
            job_desc_path = Path(job_desc_path).resolve()

            if not resumes_folder.exists():
                print(f"Resumes folder not found: {resumes_folder}")
                return None

            if not job_desc_path.exists():
                print(f"Job description file not found: {job_desc_path}")
                return None

            # Read job description
            job_description_text = self.extract_text_from_pdf(job_desc_path)
            if not job_description_text:
                print("Could not extract text from job description PDF")
                return None

            job_description_tokens = self.tokenize_text(job_description_text)

            # Get all resumes from folder
            resume_files = list(resumes_folder.glob('*.pdf'))
            if not resume_files:
                print(f"No PDF resumes found in: {resumes_folder}")
                return None

            # Process job description
            job_skills = set()
            job_qualifications = set()
            for job_token, job_label in job_description_tokens:
                if job_label == 'QUALIFICATION':
                    job_qualifications.add(job_token.replace('\n', ' '))
                elif job_label == 'SKILLS':
                    job_skills.add(job_token.replace('\n', ' '))

            results_list = []
            resumes_texts = []

            # Process each resume
            for resume_path in resume_files:
                resume_text = self.extract_text_from_pdf(str(resume_path))
                resumes_texts.append(resume_text)
                resume_tokens = self.tokenize_text(resume_text)

                matched_skills = set()
                matched_qualifications = set()
                email = set()
                phone = set()

                # Match tokens
                for resume_token, resume_label in resume_tokens:
                    for job_token, job_label in job_description_tokens:
                        if resume_token.lower().replace('\n', ' ') == job_token.lower().replace('\n', ' '):
                            if resume_label == 'SKILLS':
                                matched_skills.add(resume_token.replace('\n', ' '))
                            elif resume_label == 'QUALIFICATION':
                                matched_qualifications.add(resume_token.replace('\n', ' '))
                        elif resume_label == 'PHONE' and bool(self.float_digit_regex.match(resume_token)):
                            phone.add(resume_token)

                # Extract email and phone
                email_set = set(re.findall(self.email_pattern, resume_text.replace('\n', ' ')))
                email.update(email_set)

                for email_str in list(email):
                    numberphone = self.email_with_phone_regex.search(email_str)
                    if numberphone:
                        email.remove(email_str)
                        val = numberphone.group(1) or numberphone.group(2)
                        phone.add(val)
                        email.add(email_str.strip(val))

                # Calculate similarity score
                similarity_score = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0

                # Store results
                result_dict = {
                    "Resume": resume_path.name,
                    "Similarity Score": similarity_score,
                    "Skill Matches": len(matched_skills),
                    "Matched Skills": matched_skills,
                    "CGPA": self.extract_cgpa(resume_text),
                    "Email": email,
                    "Phone": phone,
                    "Qualification Matches": len(matched_qualifications),
                    "Matched Qualifications": matched_qualifications
                }
                results_list.append(result_dict)

            # Create results DataFrame
            results_df = pd.DataFrame(results_list)
            
            # Generate and save heatmap if skills_keywords provided
            if skills_keywords:
                self.generate_skills_heatmap(resumes_texts, resume_files, skills_keywords)

            return results_df, job_skills, job_qualifications

        except Exception as e:
            print(f"Error in analyze_resumes: {str(e)}")
            return None

    def generate_skills_heatmap(self, resumes_texts, resume_files, skills_keywords):
        """Generate and save skills heatmap."""
        tagged_resumes = [TaggedDocument(words=word_tokenize(text.lower()), tags=[str(i)]) 
                         for i, text in enumerate(resumes_texts)]
        
        model = Doc2Vec(vector_size=20, min_count=2, epochs=50)
        model.build_vocab(tagged_resumes)
        model.train(tagged_resumes, total_examples=model.corpus_count, epochs=model.epochs)

        # Calculate similarity scores
        skills_similarity_scores = []
        for resume_text in resumes_texts:
            scores = []
            for skill in skills_keywords:
                vector1 = model.infer_vector(word_tokenize(resume_text.lower()))
                vector2 = model.infer_vector(word_tokenize(skill.lower()))
                similarity = model.dv.cosine_similarities(vector1, [vector2])[0]
                scores.append(similarity)
            skills_similarity_scores.append(scores)

        # Create heatmap
        plt.figure(figsize=(12, 8))
        skills_similarity_df = pd.DataFrame(
            skills_similarity_scores,
            columns=skills_keywords,
            index=[f.name for f in resume_files]
        )
        sns.heatmap(skills_similarity_df, cmap='YlGnBu', annot=True, fmt=".2f")
        plt.title('Skills Similarity Heatmap')
        plt.xlabel('Skills')
        plt.ylabel('Resumes')
        plt.tight_layout()
        plt.savefig('skills_heatmap.png')
        plt.close()

def main():
    # Initialize analyzer
    analyzer = ResumeMatchAnalyzer()
    
    # Get input from user with better path handling
    while True:
        resumes_folder = input("Enter the path to folder containing resumes: ").strip('"')
        if Path(resumes_folder).exists():
            break
        print("Folder not found. Please enter a valid path.")

    while True:
        job_desc_path = input("Enter the path to job description PDF: ").strip('"')
        if Path(job_desc_path).exists():
            break
        print("File not found. Please enter a valid path.")

    skills_input = input("Enter skills to analyze (comma-separated) or press Enter to skip: ")
    skills_keywords = [skill.strip() for skill in skills_input.split(',')] if skills_input else None
    
    # Analyze resumes
    try:
        results = analyzer.analyze_resumes(
            resumes_folder, 
            job_desc_path, 
            skills_keywords
        )
        
        if results:
            results_df, job_skills, job_qualifications = results
            
            # Print results
            print("\n=== Analysis Results ===")
            print("\nJob Requirements:")
            print(f"Required Skills: {', '.join(job_skills)}")
            print(f"Required Qualifications: {', '.join(job_qualifications)}")
            
            print("\nResume Analysis:")
            print(results_df.to_string())
            
            # Save results to Excel in the same directory as the script
            output_file = Path(__file__).parent / 'resume_analysis_results.xlsx'
            results_df.to_excel(output_file, index=False)
            print(f"\nResults saved to {output_file}")
            
            if skills_keywords:
                heatmap_file = Path(__file__).parent / 'skills_heatmap.png'
                print(f"Skills heatmap saved as '{heatmap_file}'")
                
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()