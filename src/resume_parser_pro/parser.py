import logging
from typing import Dict, Any

from .reader import ResumeReader
from .extractors.basic_fields import BasicFieldExtractor
from .extractors.experience import ExperienceExtractor
from .extractors.skills import SkillsExtractor
from .extractors.education import EducationExtractor
from .extractors.org_location import OrgLocationExtractor


class ResumeParser:
    """A production-level Resume Parser that orchestrates reading and extraction of resume information."""
    
    def __init__(self, resume_path: str, logger: logging.Logger = None):
        self.resume_path = resume_path
        self.logger = logger or logging.getLogger(__name__)

        # Initialize component extractors
        self.reader = ResumeReader(logger=self.logger)
        self.basic_extractor = BasicFieldExtractor(logger=self.logger)
        self.experience_extractor = ExperienceExtractor(logger=self.logger)
        self.skills_extractor = SkillsExtractor(logger=self.logger)
        self.edu_extractor = EducationExtractor(logger=self.logger)
        self.org_location_extractor = OrgLocationExtractor(logger=self.logger)

    def parse(self) -> Dict[str, Any]:
        """Parse the resume and return structured data."""
        self.logger.info(f"Parsing resume: {self.resume_path}")
        text = self.reader.read_resume_file(self.resume_path)

        # Extract all fields
        result = {
            "name": self.basic_extractor.extract_name(text),
            "email": self.basic_extractor.extract_email(text),
            "phone_number": self.basic_extractor.extract_phone_number(text),
            "address": self.basic_extractor.extract_address(text),
            "experience": self.experience_extractor.extract_experience(text),
            "skills": self.skills_extractor.extract_skills(text),
            "education": self.edu_extractor.extract_education(text)
        }

        # Add organization and location data
        org_location_data = self.org_location_extractor.extract(text)
        result.update(org_location_data)

        return result


if __name__ == "__main__":
    # Example usage
    resume_path = "Kumar.Abhinav.docx"
    parser = ResumeParser(resume_path)
    parsed_data = parser.parse()
    print(parsed_data)