import csv
import os

def load_recipients(file_path):
    """Loads recipient data from a CSV file and returns a list of dictionaries."""
    file_path = os.path.abspath(file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        recipients = [row for row in reader]
    
    return recipients

def validate_recipients(recipients):
    """Validates that each recipient has a non-empty 'email' field."""
    for i, recipient in enumerate(recipients, start=1):
        email = recipient.get('email', '').strip()
        if not email:
            raise ValueError(f"Row {i}: Missing email address.")
    return True

if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(__file__)
    
    # Construct path to the CSV file (relative path to 'data/mail.csv')
    recipients_file = os.path.join(script_dir, '..', '..', 'data', 'mail.csv')
    
    try:
        recipients = load_recipients(recipients_file)
        validate_recipients(recipients)
        print(f"✅ Loaded {len(recipients)} recipients successfully.")
        if recipients:
            print("📧 First recipient:", recipients[0])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
