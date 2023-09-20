from dotenv import load_dotenv
import os
import logging
import json
import boto3

# Load environment variables from .env file
load_dotenv()

# Get secrets either from environment variables or AWS Secrets Manager
def get_secrets():
    # Try fetching secrets from AWS Secrets Manager
    try:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=os.environ.get('SECRETS_NAME', 'google_calendar_api_secrets_1'))
        secrets = json.loads(response['SecretString'])
        return secrets
    except Exception as e:
        # If there's an issue (like not being on AWS or lacking permissions), fetch from environment variables
        secrets = {key: os.getenv(key) for key in os.environ if key.startswith("CRED_") or key in ['SUBJECT_EMAIL', 'CALENDAR_ID']}
        return secrets

secrets = get_secrets()

# Extract secrets from the obtained values
creds_data = {}
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

for key in keys:
    creds_data[key] = secrets.get(f'CRED_{key}')

SUBJECT_EMAIL = secrets.get('SUBJECT_EMAIL')
if not SUBJECT_EMAIL:
    raise Exception("Please set the SUBJECT_EMAIL.")

CALENDAR_ID = secrets.get('CALENDAR_ID')
if not CALENDAR_ID:
    raise Exception("Please set the CALENDAR_ID.")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
