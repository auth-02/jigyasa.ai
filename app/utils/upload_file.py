import boto3
from fastapi import UploadFile
from base import REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_ENDPOINT_URL, BUCKET_NAME

def upload_to_S3_bucket(file: UploadFile):
    """
    Uploads a PDF file to the configured S3 bucket.
    Args:
        file (UploadFile): Uploaded PDF file.
    """
    
    s3 = boto3.client(
        "s3",
        region_name=REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=S3_ENDPOINT_URL,
    )

    pdf_key = file.filename
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, pdf_key)
        return f"PDF {pdf_key} successfully uploaded to bucket {BUCKET_NAME}."
    except Exception as e:
        return f"Error uploading PDF: {str(e)}"