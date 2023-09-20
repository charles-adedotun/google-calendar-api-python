#!/bin/bash

# Stop the script if any command fails
set -e

# Determine the directory containing this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load AWS config
CONFIG_FILE="$DIR/aws_config.json"
S3_BUCKET=$(jq -r '.s3_bucket' "$CONFIG_FILE")
REGION=$(jq -r '.region' "$CONFIG_FILE")
SECRETS_NAME=$(jq -r '.secrets_name' "$CONFIG_FILE")

# Upload secrets to AWS Secrets Manager
echo "Uploading secrets to AWS Secrets Manager..."
python "$DIR/upload_secrets.py"

# Check if the bucket exists
if ! aws s3api head-bucket --bucket $S3_BUCKET; then
    echo "Bucket does not exist, creating..."
    aws s3api create-bucket --bucket $S3_BUCKET --region $REGION
else
    echo "Bucket exists, proceeding with deployment..."
fi

# Changing directory to root of the project
cd "$DIR/.."

# Building the application
echo "Building the application..."
sam build -t "$DIR/template.yaml"

# Deploy the application
echo "Deploying the application..."
sam deploy \
    --template-file .aws-sam/build/template.yaml \
    --s3-bucket $S3_BUCKET \
    --region $REGION \
    --capabilities CAPABILITY_IAM \
    --stack-name google-calendar-api-stack \
    --parameter-overrides SecretsName=$SECRETS_NAME

# Output API Gateway URL
API_URL=$(aws cloudformation describe-stacks --stack-name google-calendar-api-stack --query 'Stacks[0].Outputs[0].OutputValue' --output text)
echo "API URL: $API_URL"
