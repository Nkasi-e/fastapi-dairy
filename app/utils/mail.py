from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from app.config import settings


config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
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
