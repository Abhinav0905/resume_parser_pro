# extractors/basic_fields.py

import re
import logging
from typing import List, Optional
import spacy
from spacy.matcher import Matcher


class BasicFieldExtractor:
    """
    Extract basic fields like name, email, phone, address, etc.
    """

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "textcat"])  
        # We only need tokenization + tagging + NER

    def extract_name(self, text: str) -> Optional[str]:
        """
        Heuristic approach: look for consecutive PROPN tokens.
        """
        self.logger.debug("Extracting name using spaCy PROPN pattern.")
        matcher = Matcher(self.nlp.vocab)

        name_patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
        ]
        matcher.add("NAME", name_patterns)

        doc = self.nlp(text)
        matches = matcher(doc)

        if not matches:
            self.logger.debug("No name pattern matched.")
            return None

        # Return the first match found
        match_id, start, end = matches[0]
        span = doc[start:end]
        self.logger.debug(f"Name found: {span.text}")
        return span.text

    def extract_email(self, text: str) -> List[str]:
        """
        Return all email addresses found in text.
        """
        email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        emails = re.findall(email_pattern, text)
        self.logger.debug(f"Emails found: {emails}")
        return emails

    def extract_phone_number(self, text: str) -> List[str]:
        """
        Return all phone numbers that match a broad regex pattern.
        """
        phone_pattern = re.compile(r"[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]")
        phones = re.findall(phone_pattern, text)
        self.logger.debug(f"Phone numbers found: {phones}")
        return phones

    def extract_address(self, text: str) -> List[str]:
        """
        Very simplistic address detection. Real addresses may need more advanced approach.
        """
        # Example pattern: "123 Main St." or "55 Market Rd."
        address_pattern = re.compile(r"\d{1,3}\s\w+\s\w+\.")
        addresses = re.findall(address_pattern, text)
        self.logger.debug(f"Addresses found: {addresses}")
        return addresses

