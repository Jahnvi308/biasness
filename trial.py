import os
import PyPDF2
import re
import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
import string

def load_text_from_pdf(file_path):
    pdf_reader = PyPDF2.PdfFileReader(file_path)
    text = ""
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extractText()
    return text

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'•|●|∙|-|\*|·', '', text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    processed_text = " ".join(tokens)
    return processed_text    

def predict_gender(text):
    # Define lists of gender-related pronouns
    male_pronouns = ["he", "him", "his", "male", "man", "men"]
    female_pronouns = ["she", "her", "hers", "female", "women"]
    
    words = text.split()  # Split text into words
    
    # Count occurrences of male and female pronouns
    male_count = sum(word.lower() in male_pronouns for word in words)
    female_count = sum(word.lower() in female_pronouns for word in words)
    
    # print(male_count)
    # print(female_count)

    if male_count > female_count:
        return "Male"
    elif female_count > male_count:
        return "Female"
    else:
        return "Unknown"

def main():
    # Specify the paths to the job description folder and resume folder
    resume_folder = "resumes"
    
    # Load the resume files
    resume_files = os.listdir(resume_folder)
    resume_paths = [os.path.join(resume_folder, resume_file) for resume_file in resume_files]
    resumes_text = []
    for resume_path in resume_paths:
        resume_text = load_text_from_pdf(resume_path)
        resume_preprocessing = preprocess_text(resume_text)
        resumes_text.append(resume_preprocessing)
    
    for resume_text in resumes_text:
        predicted_gender = predict_gender(resume_text)
        print("Predicted Gender:", predicted_gender)

if __name__ == "__main__":
    main()
