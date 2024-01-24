import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import certifi


def send_email(to_email, subject, message):
    # Your Gmail email address and password
    gmail_address = "pibotto6@gmail.com"
    app_password = "efgguhawyeuhaxcv"

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Establish a secure connection with the SMTP server
    context = ssl.create_default_context(cafile=certifi.where())

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Log in to your Gmail account
        server.login(gmail_address, app_password)

        # Send the email
        server.sendmail(gmail_address, to_email, msg.as_string())
'''
# Example usage:
to_email = "raspypi6@gmail.com"
subject = "BOTTO REFILL"
message = "CRITICAL: Refill BNB Tax and cancel order"

send_email(to_email, subject, message)
'''
