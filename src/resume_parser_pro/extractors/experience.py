# extractors/experience.py

import re
import logging
from typing import List, Dict, Any
import spacy

from resume_parser_pro.utils.text_sections import get_section


class ExperienceExtractor:
    """
    Extract structured work experience from the resume text (Work Experience, Other Experience).
    """

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "textcat"])
        # A list of job titles to help identify designations
        self.job_titles = [
            "Data Analyst", "Software Engineer", "Sr. Software Engineer", "Manager",
            "Director", "Consultant", "Tech Lead", "Project Manager",
            "Business Analyst", "Developer", "Architect", "Specialist",
            # ...
        ]
        # Common date pattern e.g. "Jan 2020 - Feb 2021"
        self.date_pattern = (
            r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
            r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)\s*\d{4}\s*(?:-|–|to)\s*(?:Present|Current|'
            r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
            r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)\s*\d{4})'
        )

    def extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """
        Top-level method to parse "Work Experience" and possibly "Other Experience" sections.
        """
        self.logger.debug("Extracting experience from text.")
        work_section = get_section(text, "Work Experience", "Other Experience", logger=self.logger)
        other_section = get_section(text, "Other Experience", "Education", logger=self.logger)
        experiences = []
        experiences.extend(self._extract_experience_entries(work_section))
        experiences.extend(self._extract_experience_entries(other_section))
        return experiences

    def _extract_experience_entries(self, section_text: str) -> List[Dict[str, Any]]:
        """
        A line-based approach that:
        1) Detects 'duration' with a date pattern.
        2) Finds job titles from a dictionary.
        3) Uses spaCy to detect ORG and location (GPE).
        4) Accumulates lines in a 'description'.
        """
        results = []
        if not section_text:
            return results

        current_exp = {}
        lines = section_text.split("\n")

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # 1) Check for date range to start a new experience block
            duration_match = re.search(self.date_pattern, line_stripped, re.IGNORECASE)
            if duration_match:
                if current_exp:
                    results.append(current_exp)
                current_exp = {
                    "duration": duration_match.group(),
                    "company": None,
                    "designation": None,
                    "location": None,
                    "description": ""
                }
                continue

            # 2) Check for known job titles
            for title in self.job_titles:
                pattern = rf"\b{re.escape(title.lower())}\b"
                if re.search(pattern, line_stripped.lower()):
                    current_exp["designation"] = title
                    break

            # 3) spaCy to detect ORG, GPE
            doc_line = self.nlp(line_stripped)
            for ent in doc_line.ents:
                if ent.label_ == "ORG" and current_exp.get("company") is None:
                    # Basic: store the first ORG you see in that block
                    current_exp["company"] = ent.text
                elif ent.label_ == "GPE" and current_exp.get("location") is None:
                    current_exp["location"] = ent.text

            # 4) Append line to 'description'
            desc = current_exp.get("description", "")
            desc += line_stripped + " "
            current_exp["description"] = desc

        if current_exp:
            results.append(current_exp)

        return results
    
    
