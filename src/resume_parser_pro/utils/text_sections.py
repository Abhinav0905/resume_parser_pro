
# resume_parser/utils/text_sections.py

import logging


def get_section(text: str, section_title: str, next_section_title: str = None, logger: logging.Logger = None) -> str:
    """
    Extract the text from `section_title` to `next_section_title` in a case-insensitive manner.
    If `next_section_title` is not found, returns everything from `section_title` to the end.
    """
    if not text or not section_title:
        return ""

    if logger:
        logger.debug(f"Extracting section from '{section_title}' to '{next_section_title}'.")

    lower_text = text.lower()
    start_idx = lower_text.find(section_title.lower())
    if start_idx == -1:
        if logger:
            logger.debug(f"Section '{section_title}' not found in text.")
        return ""

    section_text = text[start_idx:]
    if next_section_title:
        # Find the next heading
        lower_section_text = section_text.lower()
        end_idx = lower_section_text.find(next_section_title.lower())
        if end_idx != -1:
            section_text = section_text[:end_idx]

    return section_text.strip()

