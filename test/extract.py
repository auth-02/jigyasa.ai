import boto3
from pdf2image import convert_from_path
import pytesseract
import os

os.environ['TESSDATA_PREFIX'] = '/home/atharva/DΞVlove/jigyasa.ai/'

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566', 
    aws_access_key_id='jigyasa',         
    aws_secret_access_key='jigyasa'
)

def download_pdf_from_s3(bucket_name, file_key, local_path):
    """Download the PDF from a localstack S3 bucket."""
    
    s3.download_file(bucket_name, file_key, local_path)
    print(f"Downloaded {file_key} from bucket {bucket_name} to {local_path}")

def extract_text_with_ocr(pdf_path, start_page, end_page):
    """Extract Sanskrit text using OCR for problematic PDFs."""
    
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page, poppler_path='/usr/bin')
    extracted_text = []
    for img in images:
        text = pytesseract.image_to_string(img, lang="en")
        extracted_text.append(text)
    return extracted_text

def extract_sanskrit_shlokas_using_ocr(pdf_path, start_page, end_page):
    """Extract only Sanskrit text using OCR."""
    
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page, poppler_path='/usr/bin')
    sanskrit_text = []
    for img in images:
        text = pytesseract.image_to_string(img, lang="san")
        sanskrit_text.append(text)
    return sanskrit_text

# Main function
if __name__ == "__main__":
    bucket_name = "jigyasa-ai-spiritual-text"
    file_key = "Bhagvad-Gita.pdf"
    local_pdf_path = "data/raw/Bhagvad-Gita.pdf"
    start_page = 59
    end_page = 99

    # download_pdf_from_s3(bucket_name, file_key, local_pdf_path)
