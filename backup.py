import os
import zipfile # to zip
import boto3 # aws service for python
from dotenv import load_dotenv # import dotenv package
import shutil  # For removing the backup directory after zipping the backup

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION = os.getenv("AWS_REGION")

# Check if credentials are loaded
if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
    raise ValueError("AWS credentials are missing! Check your .env file.")

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,  # Required for temporary credentials
    region_name=AWS_REGION
)

# Define the directory where the backup will be saved
backup_directory = "s3_backup"
if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)

# List all buckets in the S3 account
try:
    response = s3.list_buckets()
    if 'Buckets' not in response:
        print("No S3 buckets found.")
    else:
        # Loop through each bucket
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            print(f"Backing up bucket: {bucket_name}")

            # Create a directory for this specific bucket
            bucket_backup_directory = os.path.join(backup_directory, bucket_name)
            if not os.path.exists(bucket_backup_directory):
                os.makedirs(bucket_backup_directory)

            # List the objects in the current bucket
            try:
                objects_response = s3.list_objects_v2(Bucket=bucket_name)
                if 'Contents' not in objects_response:
                    print(f"No objects found in bucket {bucket_name}.")
                else:
                    # Download each object in the bucket to the specific backup directory
                    for obj in objects_response['Contents']:
                        file_name = obj['Key']
                        print(f"Downloading {file_name} from {bucket_name}...")
                        s3.download_file(bucket_name, file_name, os.path.join(bucket_backup_directory, file_name))
                    print(f"Backup for {bucket_name} completed!")
            except Exception as e:
                print(f"Error connecting to bucket {bucket_name}: {e}")
except Exception as e:
    print("Error connecting to S3:", e)

# compress the downloaded files into a ZIP file
zip_file_name = "s3_backup.zip"
with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(backup_directory):
        for file in files:
            zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), backup_directory))

print(f"Backup has been compressed and saved as {zip_file_name}")

# Remove the original backup directory after the zip file has been created to save space (remove if you wish to keep unzipped version)
shutil.rmtree(backup_directory)
print(f"Backup folder {backup_directory} has been removed.")