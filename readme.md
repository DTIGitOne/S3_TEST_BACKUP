### BACKUP SCRIPT

`In order to run this script you will need to follow the next steps:`

1. First make sure that you have the following tools/packages installed on your device:

- Python/pip

- boto3 

- python-dotenv

## How to install (skip if you already have the mentioned packages installed)

# python/pip
To download python and pip on to your device you will have to follow the steps for your specific operating system located here: [https://www.python.org/downloads/]

# boto3
In order to install the boto3 package you will already have to have pip installed in order to download the package, to install the package run:
`pip install boto3`

# python-dotenv
In order to install the python-dotenv package you will already have to have pip installed in order to download the package, to install the package run:
`pip install python-dotenv`

2. Next make sure to add the needed credentials for AWS and S3 into your environmental variable file (.env): 

*AWS_ACCESS_KEY_ID=your_access_key*
*AWS_SECRET_ACCESS_KEY=your_secret_key*
*AWS_SESSION_TOKEN=your_session_token*
*AWS_REGION=eu-central-1*

3. The next step would be to list all of the buckets for backup inside of a `buckets.txt` file. List them in the form of bucket names listed in new rows of the .txt file.

3. The final step is to run the script and create a S3_Bucket backup file and save it as a .zip file, to execute the script run:
`python backup.py`
