import os
import base64
import logging
from typing import Optional
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Config
SCOPES = [os.getenv("Url")]  
CREDENTIALS_FILE = os.getenv("Cred_File_Path")
TOKEN_FILE = "gmail_token.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def Send_Email_Via_Gmail(subject: str, body_text: str) -> Optional[str]:
    """Async wrapper: Send an email via Gmail API and return the message ID if successful."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _send_email_blocking, subject, body_text)


def _send_email_blocking(subject: str, body_text: str) -> Optional[str]:
    """Blocking Gmail send logic (runs in executor)."""
    creds = None
    sender = "anpsujwal@gmail.com"
    to = "kollirithvik3969@gmail.com"

    # Load saved token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh or generate new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"Gmail credentials file '{CREDENTIALS_FILE}' not found.")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # Build Gmail service
    service = build("gmail", "v1", credentials=creds)

    # Create message
    message = MIMEText(body_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}

    try:
        sent_message = service.users().messages().send(userId="me", body=body).execute()
        logging.info(f"Email sent successfully to {to} | Message ID: {sent_message['id']}")
        return sent_message["id"]
    except Exception as e:
        logging.error(f"Failed to send email to {to}: {e}")
        return None



if __name__ == "__main__":
    async def main():
        subject = "Business Proposal"
        body = "Dear John,\n\nWe are pleased to share our proposal...\n\nBest regards,\nCompany Team"
        msg_id = await Send_Email_Via_Gmail(subject, body)
        print("Message ID:", msg_id)

    asyncio.run(main())