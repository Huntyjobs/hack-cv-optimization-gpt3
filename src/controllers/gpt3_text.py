from typing import Optional

from fastapi import APIRouter, status, Response, Depends

from clients.gpt3 import create_audio_text, create_text_gp3, get_models_gp3
from services.conversation import Conversation
from utils.validate_token import validate_auth_token
from settings import Settings

settings = Settings()

router = APIRouter(
    tags=["CPT3"],
    dependencies=[Depends(validate_auth_token)],
)


@router.get(
    "/create/text",
    status_code=status.HTTP_200_OK,
)
async def create(
    prompt: str,
    models: Optional[str] = "gpt-3.5-turbo",
):
    """
    > This function takes in a prompt, instructions, and models, and returns the first choice of the response

    - **param** prompt: The prompt to be used for the text generation
    - **type** prompt: str
    - **param** instructions: A string containing instructions for the user
    - **type** instructions: Optional[str]
    - **param** models: The model to use. The current available models are:
    - **type** models: Optional[str]
    - **return**: The text of the first choice.
    """
    return create_text_gp3(prompt=prompt, model=models)


@router.post(
    "/conversation",
    status_code=status.HTTP_200_OK,
)
async def get_models(prompt: str, response: Response):
    """
    It returns a list of models, either the default models or the models specified by the user

    - **param** models: A comma-separated list of models to use. If not specified, all models will be used
    - **type** models: Optional[str]
    - **return**: A list of models
    """
    conversation = Conversation()
    result = conversation.conversation_int(prompt)
    return result["choices"][0]["message"]["content"]


@router.post("/audio/transcriptions")
async def upload_file_audio(
    url_video: str,
):
    """
    > Uploads a file and returns a text transcription of the audio file

    - **param** file: UploadFile = File(...)
    - **type** file: UploadFile
    - **return**: The function create_audio_text is being returned.
    """
    return create_audio_text(url_video=url_video)


@router.get(
    "/models/list",
    status_code=status.HTTP_200_OK,
)
def get_models(models: Optional[str] = None):
    """
    It returns a list of models, either the default models or the models specified by the user

    - **param** models: A comma-separated list of models to use. If not specified, all models will be used
    - **type** models: Optional[str]
    - **return**: A list of models
    """
    return get_models_gp3(models)
