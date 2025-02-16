from typing import Dict, List, Any
import spacy
import re
from .base import BaseExtractor

class OrgLocationExtractor(BaseExtractor):
    def __init__(self, logger=None):
        super().__init__(logger)
        # Load spaCy model (assuming it's already loaded in parent class)
        self.nlp = spacy.load("en_core_web_sm")
        
        # Keywords that often precede company names in resumes
        self.company_indicators = [
            r"at\s+([A-Z][A-Za-z0-9\s&.,]+)",
            r"for\s+([A-Z][A-Za-z0-9\s&.,]+)",
            r"with\s+([A-Z][A-Za-z0-9\s&.,]+)",
            r"@\s*([A-Z][A-Za-z0-9\s&.,]+)",
            r"(?:Company|Employer):\s*([A-Z][A-Za-z0-9\s&.,]+)"
        ]
        
        # Common words to filter out from company names
        self.filter_words = {'limited', 'ltd', 'llc', 'inc', 'corporation', 'corp', 'company'}

    def clean_company_name(self, name: str) -> str:
        """Clean and standardize company names."""
        # Remove any leading/trailing whitespace and punctuation
        name = name.strip().strip('.,;')
        
        # Remove common company suffixes
        name_parts = name.lower().split()
        if name_parts and name_parts[-1] in self.filter_words:
            name = ' '.join(name.split()[:-1])
            
        return name.strip()

    def extract_companies_from_text(self, text: str) -> List[str]:
        """Extract company names using regex patterns and indicators."""
        companies = set()
        
        # Look for companies using keyword indicators
        for pattern in self.company_indicators:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                company = match.group(1)
                if company:
                    cleaned = self.clean_company_name(company)
                    if cleaned:
                        companies.add(cleaned)
        
        return list(companies)

    def extract(self, text: str) -> Dict[str, List[str]]:
        """
        Extract all organizations and locations from the resume text.
        
        Args:
            text (str): The full resume text
            
        Returns:
            Dict[str, List[str]]: Dictionary containing lists of organizations and locations
        """
        result = {
            "organizations": [],
            "locations": []
        }
        
        # Process the entire text with spaCy
        doc = self.nlp(text)
        
        # Extract organizations using spaCy NER
        for ent in doc.ents:
            if ent.label_ == "ORG":
                org_name = self.clean_company_name(ent.text)
                if org_name and org_name not in result["organizations"]:
                    result["organizations"].append(org_name)
            elif ent.label_ == "GPE":
                location = ent.text.strip()
                if location and location not in result["locations"]:
                    result["locations"].append(location)
        
        # Add companies found through regex patterns
        pattern_companies = self.extract_companies_from_text(text)
        for company in pattern_companies:
            if company not in result["organizations"]:
                result["organizations"].append(company)
        
        return result