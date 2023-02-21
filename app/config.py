from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    jwt_secret_key: str
    algorithm: str
    access_token_expires_in: int

    """ EMAIL VARIABLES """
    mail_username: str
    mail_password: str
    mail_port: int
    mail_server: str

    class Config:
        env_file = ".env"


settings = Settings()
