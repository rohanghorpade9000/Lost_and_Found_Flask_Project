import smtplib
import os
from dotenv import load_dotenv

load_dotenv()  # Load email credentials from .env file

EMAIL_SENDER = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_email(to_email, lost_item, found_item):
    """ Sends an email notification when a lost item is matched with a found item. """
    subject = "Your Lost Item Has Been Found!"
    body = f"""
    Hello,

    Your lost item has been found!

    Lost Item: {lost_item["item"]}
    Location: {lost_item["location"]}
    Date Lost: {lost_item["date"]}

    Found Item: {found_item["item"]}
    Found Location: {found_item["location"]}
    Found Date: {found_item["date"]}

    The person who found the item can be contacted at: {found_item.get("email", "No email provided")}

    Please reach out to claim your item.

    Regards,
    Lost & Found System
    """

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, message)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
