# app/ingestion/ingest.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.upload_file import upload_to_S3_bucket

router = APIRouter()

@router.post("/upload-knowledge-base")
async def upload_pdf(file: UploadFile = File(...)):
    """
    API endpoint to upload a PDF to S3.
    Args:
        file (UploadFile): Uploaded PDF file.
    Returns:
        JSON response with success or error message.
    """
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    upload_response = upload_to_S3_bucket(file)
    if "successfully uploaded" in upload_response:
        return {"message": upload_response}
    else:
        raise HTTPException(status_code=500, detail=upload_response)

