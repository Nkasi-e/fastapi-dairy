import os
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from fastapi_mail.errors import ConnectionErrors
from dotenv import load_dotenv

load_dotenv(".env")


config = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_PORT=os.environ.get("MAIL_PORT"),
    MAIL_FROM=os.environ.get("MAIL_USERNAME"),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TIMEOUT=1,
)

template = f"""

<p>{''}</p>

<h5>Hello Everyone </h5>
"""


async def send_mail(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )

    fm = FastMail(config)
    try:
        await fm.send_message(message, template_name="email.html")
        return True
    except ConnectionErrors as error:
        print(error)
        return False
