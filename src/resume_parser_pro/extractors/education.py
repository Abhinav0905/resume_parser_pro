# extractors/education.py

import re
import logging
from typing import List, Dict


class EducationExtractor:
    """Extract education data from resume text."""
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        
        self.education_keywords = {
            'degree': [
                'bachelor', 'master', 'phd', 'doctorate', 'bs', 'ba', 'btech', 'be', 'bsc',
                'mba', 'ms', 'mtech', 'ma', 'msc', 'associate', 'certification'
            ],
            'major': [
                'engineering', 'computer science', 'business', 'management', 'economics',
                'mathematics', 'physics', 'chemistry', 'biology', 'medicine', 'arts',
                'humanities', 'social science', 'law', 'accounting', 'finance', 'marketing',
                'design', 'psychology', 'sociology', 'education', 'health', 'medicine',
                'nursing', 'pharmacy', 'dentistry', 'biology', 'chemistry', 'physics',
                'mathematics', 'statistics', 'data science', 'machine learning', 'ai',
                'artificial intelligence', 'robotics', 'mechanical', 'electrical', 'civil',
                'chemical', 'industrial', 'environmental', 'aerospace', 'materials',
                'bioinformatics', 'biotechnology', 'nanotechnology', 'telecommunications',
                'networks', 'security', 'information systems', 'software engineering',
                'web development', 'mobile development', 'cloud computing', 'database',
                'systems engineering', 'computer engineering', 'computer graphics',
                'human-computer interaction', 'ui/ux design', 'product design', 'fashion',
                'interior design', 'architecture', 'urban planning', 'landscape architecture',
                'history', 'geography', 'political science', 'international relations',
                'public policy', 'public administration', 'urban studies', 'urban planning',
                'environmental studies', 'sustainability', 'climate change', 'energy',
                'renewable energy', 'water resources', 'transportation', 'logistics',
                'supply chain', 'operations', 'manufacturing', 'quality control',
                'healthcare management', 'public health', 'health informatics', 'health policy',
                'healthcare administration', 'nursing administration', 'pharmacy administration',
                'clinical research', 'medical informatics', 'health education', 'health promotion',
                'health communication', 'health economics', 'healthcare finance', 'healthcare marketing',
                'healthcare quality', 'healthcare operations', 'healthcare consulting', 'healthcare analytics',
                'healthcare technology', 'healthcare innovation', 'healthcare entrepreneurship', 'healthcare law',
                'healthcare ethics', 'healthcare compliance', 'healthcare regulation', 'healthcare policy',
                'healthcare reform', 'healthcare delivery', 'healthcare systems', 'healthcare services',
                'healthcare networks', 'healthcare partnerships', 'healthcare mergers', 'healthcare acquisitions',
                'healthcare investments', 'healthcare startups', 'healthcare incubators', 'healthcare accelerators',
                'healthcare associations', 'healthcare organizations', 'healthcare institutions', 'healthcare agencies',
                'business administration', 'business management', 'business analytics', 'business intelligence',
                'data analytics', 'data science', 'data engineering', 'data management', 'data governance',
                'data quality', 'data integration', 'data warehousing', 'data mining', 'big data',
                'statistics', 'quantitative analysis', 'predictive modeling', 'machine learning',
                'artificial intelligence', 'deep learning', 'neural networks', 'natural language processing'],

        }

    def extract_education(self, text: str) -> List[Dict]:
        """
        Extract education information from text.
        Returns list of dicts with degree, university, year, etc.
        """
        education_data = []
        
        # Extract education section
        education_section = self._get_education_section(text)
        if not education_section:
            return education_data

        # Split into individual entries
        entries = education_section.split('\n')
        
        for entry in entries:
            if any(keyword in entry.lower() for keyword in self.education_keywords['degree']):
                edu_item = self._parse_education_entry(entry)
                if edu_item:
                    education_data.append(edu_item)
                    
        return education_data

    def _get_education_section(self, text: str) -> str:
        """Extract education section using common headers."""
        education_headers = ['education', 'academic background', 'academic qualification']
        text_lower = text.lower()
        
        for header in education_headers:
            if header in text_lower:
                start_idx = text_lower.find(header)
                # Find next section header or use end of text
                next_section = re.search(r'\n\s*([A-Z][A-Za-z\s]+:?)\s*\n', text[start_idx+len(header):])
                end_idx = next_section.start() + start_idx + len(header) if next_section else len(text)
                return text[start_idx:end_idx]
        return ""

    def _parse_education_entry(self, entry: str) -> Dict:
        """Parse individual education entry into structured data."""
        result = {}
        
        # Extract degree
        degree_pattern = r'(?i)(?:bachelor|master|phd|doctorate|bs|ba|btech|be|bsc|mba|ms|mtech|ma|msc)[s]?\s(?:of|in)?\s?(?:science|engineering|technology|arts|business|administration)?'
        degree_match = re.search(degree_pattern, entry, re.IGNORECASE)
        if degree_match:
            result['degree'] = degree_match.group().strip()
            
        # Extract university
        univ_pattern = r'(?i)(?:university|institute|college|school) (?:of )?\w+'
        univ_match = re.search(univ_pattern, entry)
        if univ_match:
            result['university'] = univ_match.group().strip()
            
        # Extract year
        year_pattern = r'(?:19|20)\d{2}'
        year_match = re.search(year_pattern, entry)
        if year_match:
            result['year'] = year_match.group()
            
        return result if result else None
