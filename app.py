import hashlib
import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import logging

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PDF_URL = os.environ['PDF_URL']
EMAIL_USERNAME = os.environ['EMAIL_USERNAME']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_BCC_LIST = os.environ['EMAIL_BCC_LIST'].split(',')
EMAIL_SUBJECT = 'ATFM Daily Plan Update'
EMAIL_BODY = 'Please see the updated ATFM Daily Plan.'

# Global variable to store the hash of the last downloaded PDF
last_pdf_hash = None

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def check_for_new_pdf():
    global last_pdf_hash

    # Download the PDF file
    logging.info('Downloading PDF file...')
    response = requests.get(PDF_URL)

    # Calculate the hash of the PDF file
    pdf_hash = hashlib.md5(response.content).hexdigest()

    if pdf_hash != last_pdf_hash:
        # If the hash has changed, update the last_pdf_hash variable
        last_pdf_hash = pdf_hash

        # Create an email message with the PDF file attached
        logging.info('PDF file has changed, sending email...')
        message = MIMEMultipart()
        message['From'] = EMAIL_USERNAME
        message['Bcc'] = ', '.join(EMAIL_BCC_LIST)
        message['Subject'] = EMAIL_SUBJECT
        message.attach(MIMEText(EMAIL_BODY))

        with open('ATFM_Daily_Plan.pdf', 'wb') as f:
            f.write(response.content)

        with open('ATFM_Daily_Plan.pdf', 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename='ATFM_Daily_Plan.pdf')
            message.attach(attachment)

        # Send the email
        with smtplib.SMTP('smtp.office365.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            smtp.send_message(message)
        logging.info('Email sent!')

if __name__ == '__main__':
    # Set up logging to file
    file_handler = logging.FileHandler('atfm_bot.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)

    while True:
        check_for_new_pdf()
        time.sleep(1800)  # Wait for 30 minutes before checking again
