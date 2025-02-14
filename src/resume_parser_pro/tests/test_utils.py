# Make a ResumeParser class that takes a resume word or pdf and parses it into a dictionary of fields.

import os
import re
import docx as docx_lib
import PyPDF2
#from pdfminer.high_level import extract_text
from typing import Dict
import spacy
from spacy.matcher import Matcher


class ResumeParser:
    def __init__(self, resume_path: str) -> None:
        self.resume_path = resume_path
  
    @staticmethod
    def read_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            for page in range(reader.numPages):
                text += reader.getPage(page).extractText()
            return text
    
    @staticmethod 
    def read_docx(file_path: str) -> str:
        document = docx_lib.Document(file_path)
        full_text = []
        for para in document.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    def read_resume_file(self) -> str:
        if not os.path.exists(self.resume_path):
            raise FileNotFoundError("File not found")
        if self.resume_path.endswith('.pdf'):
            return self.read_pdf(self.resume_path)
        elif self.resume_path.endswith('.docx'):
            return self.read_docx(self.resume_path)
        else:
            raise ValueError("File type not supported")
    
    def extract_name(self, resume_text: str) -> str:
        nlp = spacy.load('en_core_web_sm')
        matcher = Matcher(nlp.vocab)

        # Define name patterns
        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
            # Add more patterns as needed
        ]

        for pattern in patterns:
            matcher.add('NAME', patterns=[pattern])

        doc = nlp(resume_text)
        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text

        return None

    # def extract_name(self, text: str) -> str:
    #     name = re.findall(r'[\w]+', text)
    #     return name
  
    def extract_email(self, text: str) -> str:
        email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        email = re.findall(email_pattern, text)
        return email
    
    def extract_phone_number(self, text: str) -> str:
        phone_number = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        return phone_number
    
    def extract_address(self, text: str) -> str:
        address = re.findall(r'\d{1,3}\s\w+\s\w+\.', text)
        return address
    
    # how to extract other fields like education, experience, skills etc using spacy or ntlk
    def extract_education(self, text: str) -> str:
        education = []
        # Use regex pattern to find education information
        pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
        matches = re.findall(pattern, text)
        for match in matches:
            education.append(match.strip())

        return education
    
    def extract_skills(self, text: str) -> str:
        skills_list = ['Python', 'Java', 'C++', 'C#', 'JavaScript', 'Ruby', 'R', 'SQL', 'HTML', 'CSS', 'PHP', 'Swift', 
        'Objective-C', 'Kotlin', 'TypeScript', 'Scala', 'Perl', 'Go', 'Shell', 
        'PowerShell', 'Bash', 'MATLAB', 'PL/SQL', 'Visual Basic', 'VBA', 'Dart', 'Lua', 'Groovy', 'Assembly', 
        'Rust', 'Haskell', 'Julia', 'COBOL', 'F#', 'Erlang', 'Clojure', 'Apex', 'ABAP', 'Crystal', 'D', 
        'Fortran', 'Lisp', 'Logo', 'Pascal', 'Prolog', 'Scratch', 'Smalltalk', 'Turing', 'VHDL', 
        'Verilog', 'LabVIEW', 'Ada', 'ActionScript', 'ALGOL', 'Alice', 'APL', 'AWK', 'BCPL', 'Boo', 'C', 
        'Ch', 'ChucK', 'Clipper', 'ColdFusion', 'Common Lisp', 'DIBOL', 'Eiffel', 
        'Elixir', 'Elm', 'Emacs Lisp', 'Euphoria']
        skills = []
        for skill in skills_list:
            pattern = r"\b{}\b".format(re.escape(skill))
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                skills.append(skill)

        return skills

    def extract_experience(self, text: str) -> str:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        job_titles = ["engineer", "Develpor", "Analyst", "Manager", "Director", "Designer", "Architect", "Consultant", "Specialist",
                        "Administrator", "Coordinator", "Officer", "Representative", "Technician", "Assistant", "Associate", "Executive",
                        "Supervisor", "Coordinator", "Operator", "Planner", "Leader", "Technologist", "Scientist", "Researcher", "Instructor",
                        "Educator", "Trainer", "Coach", "Counselor", "Therapist", "Advisor", "Agent", "Broker", "Auditor", "Accountant",
                        "Controller", "Clerk", "Secretary", "Receptionist", "Assistant", "Aide", "Specialist", "Technician", "Engineer",
                        "Analyst", "Consultant", "Representative", "Associate", "Administrator", "Coordinator", "Manager", "Director",
                        "Business Analyst", "Data Analyst", "Financial Analyst", "Systems Analyst", "Programmer", "Developer", "Software Engineer",
                        "Web Developer", "Front-End Developer", "Back-End Developer", "Full-Stack Developer", "Mobile Developer", "iOS Developer",
                        "Android Developer", "Java Developer", "Python Developer", "Ruby Developer", "C++ Developer", "C# Developer", "JavaScript Developer",
                        "PHP Developer", "SQL Developer", "Database Developer", "Data Scientist", "Machine Learning Engineer", "AI Engineer", "Computer Scientist",
                        "Network Engineer", "Security Engineer", "DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer", "Solutions Architect",
                        "Enterprise Architect", "Technical Architect", "Infrastructure Architect", "Security Architect", "Business Architect", "Data Architect",
                        "Software Architect", "UX Designer", "UI Designer", "Graphic Designer", "Product Designer", "Interaction Designer", "Visual Designer",
                        "Motion Designer", "Industrial Designer", "Interior Designer", "Architectural Designer", "Fashion Designer", "Game Designer",
                        "Design Engineer", "Design Manager", "Design Director", "Design Lead", "Design Consultant", "Design Specialist", "Design Architect",
                        "mechanical engineer", "electrical engineer", "civil engineer", "chemical engineer", "industrial engineer", "aerospace engineer",
                        "biomedical engineer", "environmental engineer", "materials engineer", "nuclear engineer", "software engineer", "computer engineer",
                        "systems engineer", "network engineer", "security engineer", "quality engineer", "process engineer", "manufacturing engineer",
                        "production engineer", "project engineer", "engineering manager", "engineering director", "engineering lead", "engineering consultant",
                        "engineering specialist", "engineering architect", "engineering coordinator", "engineering supervisor", "engineering technician",
                        "engineering assistant", "engineering associate", "engineering officer", "engineering representative", "engineering analyst",
                        "engineering designer", "engineering scientist", "engineering researcher", "engineering instructor", "engineering educator",
                        "engineering trainer", "engineering coach", "engineering counselor", "engineering therapist", "engineering advisor", "engineering agent",
                        "HR Manager", "HR Director", "HR Business Partner", "HR Generalist", "HR Specialist", "HR Coordinator", "HR Administrator", "HR Assistant",
                        "HR Associate", "HR Officer", "HR Representative", "HR Analyst", "HR Consultant", "HR Executive", "HR Supervisor", "HR Coordinator",
                        "HR Operator", "HR Planner", "HR Leader", "HR Technologist", "HR Scientist", "HR Researcher", "HR Instructor", "HR Educator", "HR Trainer",
                        "Sr.Manager", "Sr.Developer", "Sr.Analyst", "Sr.Manager", "Sr.Director", "Sr.Designer", "Sr.Architect", "Sr.Consultant", "Sr.Specialist",
                        "Sr.Administrator", "Sr.Coordinator", "Sr.Officer", "Sr.Representative", "Sr.Technician", "Sr.Assistant", "Sr.Associate", "Sr.Executive",
                        "Sr.Supervisor", "Sr.Coordinator", "Sr.Operator", "Sr.Planner", "Sr.Leader", "Sr.Technologist", "Sr.Scientist", "Sr.Researcher", "Sr.Instructor",]
                        
        # Date patterns
        date_pattern = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
        date_pattern += r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
        date_pattern += r'Dec(?:ember)?)\s*\d{4}\s*(?:-|–|to)\s*(?:Present|Current|'
        date_pattern += r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
        date_pattern += r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
        date_pattern += r'Dec(?:ember)?)\s*\d{4})'

        experiences = []
        current_experiences = {}

        # Split text into lines
        lines = text.split('\n')

        for i, lines in enumerate(lines):
            # check for duration patters in the line
            duration_match = re.search(date_pattern, lines)
            if duration_match:
                if current_experiences:
                    experiences.append(current_experiences)
                current_experiences = {'duration': duration_match.group()}

        # Look for job titles in the same line
        for title in job_titles:
            if title in lines.lower() or (i > 0 and title in lines[i-1].lower()):
                title_match = re.search(f".*({title}).*", lines, re.IGNORECASE)
                if title_match:
                    current_experiences['designation'] = title_match.group()
                    break
        
        # Look for company name using spacy
        doc = nlp(lines)
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                current_experiences['company'] = ent.text
                break
        
        # Look for location using spacy
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                current_experiences['location'] = ent.text
                break
        
        # Look for description
        if current_experiences:
            current_experiences['description'] = lines

        # Append the last experience
        if current_experiences:
            experiences.append(current_experiences)
        
        # Return the extracted experiences
        return experiences
    
    def parse(self) -> Dict[str, str]:
        text = self.read_resume_file()
        name = self.extract_name(text)
        email = self.extract_email(text)
        phone_number = self.extract_phone_number(text)
        address = self.extract_address(text)
        education = self.extract_education(text)
        experience = self.extract_experience(text)
        skills = self.extract_skills(text)
        return {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "education": education,
            "experience": experience,
            "skills": skills
        }


resume_path = "path/to/your/resume.pdf"  # Replace with actual path to resume file
cv_parser = ResumeParser(resume_path)


