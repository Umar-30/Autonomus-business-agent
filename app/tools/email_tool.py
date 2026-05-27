import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_email(to: str, subject: str, body: str):
    """Sends a real email via SMTP."""
    if not all([SMTP_USER, SMTP_PASSWORD]):
        print("[TOOL] SMTP credentials missing. Simulating email instead.")
        return f"Simulated Email to {to}: Subject: {subject} | Body: {body[:50]}..."

    try:
        print(f"[TOOL] Sending real email to: {to}")
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        return f"Successfully sent real email to {to}"

    except Exception as e:
        return f"Error sending email: {str(e)}"
