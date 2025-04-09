from data_manager import load_recipients;
from data_manager import validate_recipients;

if __name__ == "__main__":
    recipients = load_recipients("../../local/data/mail.csv")
    validate_recipients(recipients)
    print("All recipients are valid.")

