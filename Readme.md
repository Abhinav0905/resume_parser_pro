# README.md

# Resume Parser Pro

A Python package for parsing resumes and extracting structured information from them.

## Features

- **Contact Information**: Easily extract name, email addresses, and phone numbers.
- **Work Experience**: Parse job titles, company names, durations, and locations.
- **Education**: Identify degrees, institutions, and graduation years.
- **Structured Data Output**: Returns a Python dictionary (or JSON) of parsed data for easy integration.

## Installation

You can install the package using pip:

```bash
pip install resume_parser_pro
```

## Usage

from resume_parser_pro import ResumeParser

parser = ResumeParser()

data = parser.parse('path/to/resume.pdf')
print(data)

### Project Structure
The project includes the following languages and frameworks:  
Python 3.8

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.  

### License
This project is licensed under the MIT License - see the LICENSE file for details.

