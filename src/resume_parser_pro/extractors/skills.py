# extractors/skills.py

import re
import logging
from typing import List


class SkillsExtractor:
    """
    Extract skill keywords from the resume text.
    """

    def __init__(self, known_skills: List[str] = None, logger: logging.Logger = None):
        """
        :param known_skills: A list of known skill strings to search for.
        :param logger: Optional logger instance.
        """
        self.logger = logger or logging.getLogger(__name__)
        if known_skills is None:
            known_skills = [
                "Python", "Java", "C++", "C#", "JavaScript", "Ruby", "R", "SQL", "HTML",
                "CSS", "PHP", "Swift", "Kotlin", "TypeScript", "Scala", "Perl",
                "Go", "Shell", "Bash", "MATLAB", "Excel", "Tableau", "Power BI",
                "FastAPI", "Langchain", "Azure", "Elasticsearch", "Kibana"
                # Extend as needed
            ]
        self.known_skills = known_skills

    def extract_skills(self, text: str) -> List[str]:
        """
        A dictionary-based approach to detect known skills.
        For more advanced approaches, parse bullet-lists in the "Skills" section.
        """
        found_skills = []
        for skill in self.known_skills:
            pattern = rf"\b{re.escape(skill)}\b"
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                found_skills.append(skill)

        result = list(set(found_skills))  # remove duplicates
        self.logger.debug(f"Skills found: {result}")
        return result


