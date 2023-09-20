
# Google Calendar API Integration with FastAPI

This project provides an integration between FastAPI and Google Calendar. Through this integration, you can create, update, delete, and view upcoming events in a Google Calendar.

## Table of Contents

- [Features](#features)
- [Local Setup](#local-setup)
- [Deployment to AWS](#deployment-to-aws)
- [API Usage](#api-usage)
- [License](#license)
- [Author](#author)

## Features

- Create appointments in Google Calendar.
- Update existing appointments.
- Delete appointments.
- View upcoming events.

## Local Setup

### Prerequisites

1. Python 3.10+
2. FastAPI
3. Uvicorn
4. Google Cloud SDK (for Google Calendar Authentication)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-github-username/google-calendar-fastapi.git
   cd google-calendar-fastapi
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory using `.env.sample` as a template and populate the required fields. The variables include:
   - `CALENDAR_ID`: Your Google Calendar ID.
   - `SUBJECT_EMAIL`: The email of the user you want to impersonate for Google Calendar operations.
   - Credentials from `credentials.json` obtained from Google Cloud Console. Ensure to fill in the `CRED_` prefixed variables accordingly.

5. **Run the application locally**:
   ```bash
   uvicorn main:app --reload
   ```

## Deployment to AWS

### Prerequisites

1. AWS CLI installed and configured.
2. SAM CLI.

### Deployment Steps

1. **Prepare AWS Configuration**:
   Populate the `aws_config.json` in the `deploy` directory with your AWS bucket name, region, and secret name.

2. **Upload Secrets**:
   Use the `upload_secrets.py` script to push your Google Calendar API secrets to AWS Secrets Manager.

3. **Run Deployment Script**:
   ```bash
   cd deploy
   ./deploy.sh
   ```

4. At the end of the deployment, the script will output the API Gateway URL. Take note of this as it will be your endpoint for the deployed API.

## API Usage

### Headers

Every request must include the `x-api-key` header for authentication.

### Endpoints

1. **Create Appointment**:
   - Method: POST
   - Endpoint: `/calendar/create-appointment/`
   - Body: { "attendee_email": "example@example.com", "desired_start": "2023-09-18T07:00:00", "time_zone": "America/Chicago" }
   
2. **Update Appointment**:
   - Method: POST
   - Endpoint: `/calendar/update-appointment/`
   - Body: { "event_id": "your_event_id", "new_start": "new_start_time", "time_zone": "new_time_zone" }

3. **Delete Appointment**:
   - Method: DELETE
   - Endpoint: `/calendar/delete-appointment/`
   - Body: { "event_id": "your_event_id" }

4. **View Upcoming Events**:
   - Method: GET
   - Endpoint: `/calendar/upcoming-events/`

## License

This project is licensed under the MIT License.

## Author

Charles Adedotun
