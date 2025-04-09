import boto3
import os
from core.data_manager import load_recipients
from core.template_manager import render_template
from botocore.exceptions import BotoCoreError, ClientError

# Config from environment
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'a_verified_email@example.com')
RECIPIENTS_FILE = os.getenv('RECIPIENTS_FILE_PATH', 'data/mail.csv')

# Initialize boto3 client for SES
client = boto3.client('ses', region_name=AWS_REGION)

def send_email(recipient_email, subject, body_html, body_text="This email requires an HTML-compatible email client."):
    """Send a single email via Amazon SES."""
    try:
        response = client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': body_text},
                    'Html': {'Data': body_html}
                }
            }
        )
        return response
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to send email to {recipient_email}: {str(e)}")

def main():
    subject = "Welcome to Our Service"
    try:
        recipients = load_recipients(RECIPIENTS_FILE)
    except Exception as e:
        print(f"❌ Failed to load recipients: {e}")
        return

    success_count = 0
    for recipient in recipients:
        email = recipient.get('email', '').strip()
        if not email:
            print("⚠️ Skipping recipient without email.")
            continue

        context = {"name": recipient.get('name', 'Valued Customer')}
        try:
            body = render_template("welcome_email.html", context)
            response = send_email(email, subject, body)
            print(f"✅ Email sent to {email}! Message ID: {response['MessageId']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Could not send email to {email}: {e}")

    print(f"\n📬 {success_count}/{len(recipients)} emails sent successfully.")

if __name__ == "__main__":
    main()
