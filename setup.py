from setuptools import setup, find_packages

setup(
    name='resume_parser_pro',
    version='1.0.2',
    author='Kumar Abhinav',
    author_email='rushtoabhinavin@gmail.com',
    description='A package for parsing resumes and extracting structured data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Abhinav0905/resume_parser_pro',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'spacy',
       'python-docx',
        'PyPDF2',
    ],
)

