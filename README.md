# Serverless S3 File Handler

One of the common entry points of data into a system is a file upload - via browser, FTP, email, or other means.
We separate out the processing of the file from the receipt of the file by using a Lambda function triggered by a file’s arrival.
This task is to write the handler and set up the serverless.yml file to deploy it.

## Install Serverless Framework
npm install -g serverless

## Clone the source code
- git clone https://github.com/softdev1029/serverless-file-handler
- cd src

## Make a virtual environment for Python
virtualenv venv --python=python3
source venv/bin/activate

## Install the necessary Python packages for AWS
- pip install boto3
- pip freeze > requirements.txt

## Setup the AWS credentials for Serverless frameowrk
serverless config credentials --provider aws --key <YOUR_KEY> --secret <YOUR_SECRET>

## Deploy the serverless service
serverless deploy -v
