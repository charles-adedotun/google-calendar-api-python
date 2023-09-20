import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("../.env")

# Load AWS config
with open("aws_config.json", "r") as f:
    config = json.load(f)

secrets_name = config['secrets_name']

# Extract secrets from .env
secrets = {key: os.getenv(key) for key in os.environ if key.startswith("CRED_") or key in ['SUBJECT_EMAIL', 'CALENDAR_ID']}

# Initialize Secrets Manager client
client = boto3.client('secretsmanager', region_name=config['region'])

# Check if the secret already exists
try:
    client.describe_secret(SecretId=secrets_name)
except client.exceptions.ResourceNotFoundException:
    # If it doesn't exist, create it
    client.create_secret(Name=secrets_name, Description="Secrets for the Google Calendar API application")

# Update (or set) the secret's value
response = client.put_secret_value(
    SecretId=secrets_name,
    SecretString=json.dumps(secrets)
)

print(f"Uploaded secrets to {secrets_name}")
