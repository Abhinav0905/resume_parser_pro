from typing import Dict, List, Any
import spacy
from .base import BaseExtractor

class OrgLocationExtractor(BaseExtractor):
    def __init__(self, logger=None):
        super().__init__(logger)
        # Load spaCy model (assuming it's already loaded in parent class)
        self.nlp = spacy.load("en_core_web_sm")

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
        
        # Extract organizations and locations from named entities
        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Remove duplicates and clean the organization name
                org_name = ent.text.strip()
                if org_name and org_name not in result["organizations"]:
                    result["organizations"].append(org_name)
            elif ent.label_ == "GPE":
                # Remove duplicates and clean the location name
                location = ent.text.strip()
                if location and location not in result["locations"]:
                    result["locations"].append(location)
        
        return result 