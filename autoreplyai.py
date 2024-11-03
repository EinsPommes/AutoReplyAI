import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import openai
from dotenv import load_dotenv

load_dotenv()

IMAP_SERVER = 'imap.web.de'
SMTP_SERVER = 'smtp.web.de'
EMAIL_ACCOUNT = os.environ.get('EMAIL_ACCOUNT')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if not EMAIL_ACCOUNT or not EMAIL_PASSWORD or not OPENAI_API_KEY:
    raise ValueError("Bitte stellen Sie sicher, dass EMAIL_ACCOUNT, EMAIL_PASSWORD und OPENAI_API_KEY als Umgebungsvariablen gesetzt sind.")

openai.api_key = OPENAI_API_KEY


def generate_ai_reply(email_content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent, der höfliche und professionelle E-Mail-Antworten verfasst."},
            {"role": "user", "content": email_content}
        ],
        max_tokens=150,
    )
    reply = response['choices'][0]['message']['content']
    return reply


def check_inbox():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    try:
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select('inbox')

        status, response = mail.search(None, '(UNSEEN)')
        if status != 'OK':
            print("Fehler beim Abrufen der E-Mails")
            return

        unread_msg_nums = response[0].split()

        for e_id in unread_msg_nums:
            status, data = mail.fetch(e_id, '(RFC822)')
            if status != 'OK':
                print(f"Fehler beim Abrufen der E-Mail mit ID {e_id}")
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            email_from = email.utils.parseaddr(msg['From'])[1]
            email_subject = msg['Subject']
            email_body = ''

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain' and not part.get('Content-Disposition'):
                        try:
                            email_body += part.get_payload(decode=True).decode()
                        except (UnicodeDecodeError, AttributeError):
                            email_body += part.get_payload(decode=True).decode('latin-1', errors='ignore')
            else:
                email_body = msg.get_payload(decode=True).decode()

            print(f'Neue E-Mail von: {email_from} mit Betreff: {email_subject}')

            ai_reply = generate_ai_reply(email_body)
            send_auto_reply(email_from, ai_reply, email_subject)
    except imaplib.IMAP4.error as e:
        print(f"IMAP-Fehler: {str(e)}")
    finally:
        mail.logout()


def send_auto_reply(to_address, reply_content, original_subject):
    try:
        with smtplib.SMTP(SMTP_SERVER, 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

            msg = MIMEMultipart()
            msg['From'] = EMAIL_ACCOUNT
            msg['To'] = to_address
            msg['Subject'] = f'Re: {original_subject}'

            msg.attach(MIMEText(reply_content + '\n\nDiese E-Mail wurde von Kira Assistent geschickt.', 'plain'))

            smtp.sendmail(EMAIL_ACCOUNT, to_address, msg.as_string())
        print(f'Automatische Antwort gesendet an: {to_address}')
    except smtplib.SMTPException as e:
        print(f'Fehler beim Senden der Antwort: {str(e)}')


if __name__ == "__main__":
    check_inbox()
