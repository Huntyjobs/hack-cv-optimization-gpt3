from typing import Optional

from fastapi import APIRouter, File, UploadFile, Depends

from services.conversation import ctl_data
from services.read_file import process_document
from utils.validate_token import validate_auth_token
from settings import Settings

router = APIRouter(
    tags=["text"],
    dependencies=[Depends(validate_auth_token)],
)


@router.post("/curriculum/file")
async def upload_curriculum(
    pdf: Optional[bool] = False,
    curriculum: UploadFile = File(...),
    file_english: Optional[bool] = False,
):
    """
    > This function takes a curriculum file and uploads it to the Google Cloud Platform

    - **param** pdf: Optional[bool] = False,, defaults to False
    - **type** pdf: Optional[bool] (optional)
    - **param** curriculum: UploadFile = File(...)
    - **type** curriculum: UploadFile
    - **return**: The data is being returned.
    """
    if pdf:
        data = process_document(
            file=curriculum.file,
            mime_type="application/pdf",
            project_id=Settings.PROJECT_ID,
            location=Settings.LOCATION,
            processor_id=Settings.PROCESSOR_ID,
            file_english=file_english,
        )
        ctl_data.clear()
        return data
