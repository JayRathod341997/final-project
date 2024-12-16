import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email (you need to implement the actual email logic)
def send_email(to_email, subject, body):
    from_email = "your_email@gmail.com"  # Replace with your email address
    password = "your_email_password"  # Replace with your email password or app-specific password

    # Setup email server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)

    # Prepare the email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Appointment Booking Function
