from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors
from app.config import settings


config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_PORT=settings.mail_port,
    MAIL_FROM=settings.mail_username,
    MAIL_SERVER=settings.mail_server,
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
