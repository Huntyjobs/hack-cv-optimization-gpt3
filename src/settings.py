import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MACHINE = os.getenv("MACHINE")
    if MACHINE == "GCP":
        ROOT_PATH = "/cv-optimization"
    else:
        ROOT_PATH = ""

    BASE_URL = os.getenv("BASE_URL")
    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")

    ORGANIZATION = os.getenv("YOUR_ORG_ID")
    API_KEY = os.getenv("OPENAI_API_KEY")
    PROJECT_ID = os.getenv("PROJECT_ID")
    LOCATION = os.getenv("LOCATION")
    PROCESSOR_ID = os.getenv("PROCESSOR_ID")
    HEADER_VALIDATION = os.getenv("HEADER_VALIDATION")
