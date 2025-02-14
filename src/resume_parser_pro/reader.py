# Resume Reader Class
# readers.py

import os
from typing import Dict, Any
import docx
import PyPDF2
import logging


class ResumeReaderError(Exception):
    pass


class ResumeReader:
    """
    A class to read resume files and extract information from them.
    """
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger

    def read_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Read a PDF file and extract information from it.

        """
        if self.logger:
            self.logger.info(f"Reading PDF file: {file_path}")

        text = []
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num in range(len(reader.pages)):
                    page_obj = reader.pages[page_num]
                    page_text = page_obj.extract_text()
                    text.append(page_text)
        except PyPDF2.errors.PdfReadError as e:
            self.logger.error(f"Error reading PDF file: {file_path} : {e}")
            raise ResumeReaderError(f"Error reading PDF file: {file_path}")

        except Exception as ex:
            self.logger.error(f"Error reading PDF File : {file_path} : {ex}")
            raise ResumeReaderError(f"Error reading PDF file: {file_path}")
        
        return "\n".join(text)
    
    def read_docx(self, file_path: str) -> Dict[str, Any]:
        """
        Read a Docx file and extract information from it.
        """
        if self.logger:
            self.logger.info(f"Reading DOCX file: {file_path}")

        text = []
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text.append(para.text)
        except Exception as ex:
            self.logger.error(f"Error reading DOCX file: {file_path} : {ex}")
            raise ResumeReaderError(f"Error reading DOCX file: {file_path}")

        return "\n".join(text)
    
    def read_resume_file(self, file_path: str) -> str:
        """
        Determine  the file type and read  the resume into a string.
        """
        if not os.path.exists(file_path):
            msg = f"File not found: {file_path}"
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        _, ext = os.path.splitext(file_path.lower())
        if ext == ".pdf":
            return self.read_pdf(file_path)
        elif ext == ".docx":
            return self.read_docx(file_path)
        else:
            msg = f"Unsupported file type: {ext}"
            self.logger.error(msg)
            raise ResumeReaderError(msg)

