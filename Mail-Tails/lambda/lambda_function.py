import json
import boto3
import csv
import io

s3 = boto3.client('s3')
ses = boto3.client('ses')

SENDER_EMAIL = 'facumorales2908@gmail.com'

def lambda_handler(event, context):
    # Extract event details
    try:
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
        event_name = record['eventName']
    except KeyError as e:
        print(f"❌ Error extracting event data: {e}")
        return {'statusCode': 400, 'body': json.dumps('Invalid event structure')}

    print(f"📦 Event: {event_name} | Bucket: {bucket_name} | File: {file_key}")
    
    # Load and parse CSV
    recipients = []
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response['Body'].read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(csv_content))

        for i, row in enumerate(reader, start=1):
            email = row.get('email', '').strip()
            if email:
                recipients.append(email)
            else:
                print(f"⚠️ Row {i} missing valid 'email' field: {row}")
                
    except Exception as e:
        print(f"❌ Error processing S3 object: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps('Error reading CSV file from S3')}

    if not recipients:
        print("⚠️ No valid recipients found in CSV.")
        return {'statusCode': 200, 'body': json.dumps('No recipients to process')}

    # Prepare email content
    if "PutObject" in event_name:
        subject = "🎉 The service is live!"
        body = "Welcome to our service! We're excited to have you on board."
    elif "DeleteObject" in event_name:
        subject = "⚠️ You have been removed from the service"
        body = f"The object '{file_key}' was deleted from '{bucket_name}'. You've been unsubscribed."
    else:
        print("ℹ️ Unhandled event type.")
        return {'statusCode': 200, 'body': json.dumps('Event type not supported')}

    # Send emails
    success = 0
    for email in recipients:
        try:
            response = ses.send_email(
                Source=SENDER_EMAIL,
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            print(f"✅ Email sent to {email}! Message ID: {response['MessageId']}")
            success += 1
        except Exception as e:
            print(f"❌ Error sending to {email}: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps(f"Processed event. Emails sent: {success}/{len(recipients)}")
    }
