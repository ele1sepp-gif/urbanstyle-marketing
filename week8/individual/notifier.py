import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email_notification(subject, message):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("EMAIL_SENDER, EMAIL_PASSWORD või EMAIL_RECEIVER puudub .env failist.")
        return

    try:
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.sendmail(sender, [receiver], msg.as_string())

        print("Email teavitus saadetud edukalt.")

    except Exception as e:
        print(f"Viga emaili saatmisel: {e}")