# Manual testing for the resume parser

# Importing the required libraries
from resume_parser import cv_parser


# Test the resume parser
def main():
    resume_path = [
        'Resume_Parser_Package/resume_parser/tests/Kumar.Abhinav.docx']
    parser = cv_parser(resume_path)
    result = parser.parse()
    print(result)

    for key, value in result.items():
        print(f"{key}: {value}")
        print(value)


if __name__ == '__main__':
    main()

