from dotenv import load_dotenv
import os
import logging
import json

# Load environment variables from .env file
load_dotenv()

# List of expected keys for the credentials
keys = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
    "universe_domain"
]

# Initialize an empty creds_data dictionary
creds_data = {}

# Check if credentials.json exists
if os.path.exists('credentials.json'):
    # Load credentials.json
    with open('credentials.json', 'r') as f:
        creds_data = json.load(f)
else:
    # Fetch credentials from environment variables if credentials.json does not exist
    for key in keys:
        creds_data[key] = os.getenv(f'CRED_{key}')

SUBJECT_EMAIL = os.environ.get('SUBJECT_EMAIL')
if not SUBJECT_EMAIL:
    raise Exception("Please set the SUBJECT_EMAIL environment variable.")

CALENDAR_ID = os.environ.get('CALENDAR_ID')
if not CALENDAR_ID:
    raise Exception("Please set the CALENDAR_ID environment variable.")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
