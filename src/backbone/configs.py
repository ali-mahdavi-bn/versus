from pathlib import Path

from pydantic_settings import BaseSettings




class Config(BaseSettings):
    PDF_WEB: str = "data_file/pdf_web/"

    SCI_PATH: str = "https://sci-hub.wf/"

    # postgres
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_DATABASE: str = "postgres"
    POSTGRES_PORT: int = 5432

    # Redis
    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379



    class Config:
        case_sensitive = False
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        env_file = f"{str(BASE_DIR)}/.env".replace("//", "/")
        env_file_encoding = 'utf-8'




config = Config()


class PasswordConfig:
    MIN_LENGTH = 8
    UPPERCASE_REQUIRED = False
    LOWERCASE_REQUIRED = True
    DIGIT_REQUIRED = True
    SPECIAL_CHARACTERS_REQUIRED = False
    SPECIAL_CHARACTERS = r"[!@#$%^&*()]"
