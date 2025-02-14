# Base Extractor class for Resume Parser
from logging import Logger

class BaseExtractor:
    def __init__(self, logger: Logger = None):
        self.logger = logger