import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
load_dotenv()
import os
def upload_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path.split("/")[-1]

    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to {bucket_name}/{object_name}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

file_path_to_upload = "msg.py"

s3_bucket_name = os.getenv("S3_BUCKET_NAME")

upload_to_s3(file_path_to_upload, s3_bucket_name)
