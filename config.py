from dotenv import load_dotenv
import os
import logging
import json

# Load environment variables from .env file
load_dotenv()

# Load credentials
with open('credentials.json', 'r') as f:
    creds_data = json.load(f)

SUBJECT_EMAIL = os.environ.get('SUBJECT_EMAIL')
if not SUBJECT_EMAIL:
    raise Exception("Please set the SUBJECT_EMAIL environment variable.")

CALENDAR_ID = os.environ.get('CALENDAR_ID')
if not CALENDAR_ID:
    raise Exception("Please set the CALENDAR_ID environment variable.")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
