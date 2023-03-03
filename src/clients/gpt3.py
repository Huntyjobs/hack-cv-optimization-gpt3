import pytube
import whisper
import logging

import requests
from fastapi import HTTPException, UploadFile, status

from settings import Settings

setting_var = Settings


def create_text_gp3(prompt: str, model: str):
    """
    It takes a prompt and instructions and returns a JSON object with a completion_id

    :param prompt: The prompt is the text that you want to generate a response for
    :type prompt: str
    :param instructions: This is the text that will be displayed above the prompt
    :type instructions: str
    :param model: The model is the name of the model you want to use to generate the response
    :type model: str
    :return: The response is a JSON object with the following fields:
    """
    try:
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {Settings.API_KEY}",
        }

        if model == "gpt-3.5-turbo":
            url = f"{Settings.BASE_URL}/chat/completions"
            prompt_param = "messages"
            prompt_data = [{"role": "user", "content": prompt}]
            data = True

        else:
            url = f"{Settings.BASE_URL}/completions"
            prompt_param = "prompt"
            prompt_data = prompt
            data = False

        payload = {
            prompt_param: prompt_data,
            "temperature": 0.8,
            "model": "text-davinci-003" if model is None else model,
            "max_tokens": 1800,
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        response.raise_for_status()

        if data:
            return response.json()["choices"][0]["message"]
        else:
            return response.json()["choices"][0]["text"]

    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)

    except Exception as error:
        logging.info(f"error create_text_gp3 {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"error create_text_gp3 : {error}",
        )


def create_audio_text(url_video: str):
    """
    It takes a file, sends it to the API, and returns the transcription

    :param file: The file to be transcribed
    :type file: UploadFile
    :return: A dictionary with the transcription key and the response.json() value.
    """

    try:
        data = pytube.YouTube(url_video)
        audio = data.streams.get_audio_only()
        audio.download()

        model = whisper.load_mode("large")
        text = model.transcribe(audio.default_filename)

        return text["tex"]

    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)

    except Exception as error:
        logging.info(f"error create_audio_text_ {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"error create_audio_text_ : {error}",
        )


def get_models_gp3(models):
    """
    :param models: A comma-separated list of model IDs
    :return: A list of models
    """
    try:
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {Settings.API_KEY}",
        }

        if models:
            url = f"{Settings.BASE_URL}/models{models}"
        else:
            url = f"{Settings.BASE_URL}/models"

        response = requests.request("GET", url, headers=headers)

        response.raise_for_status()

        return response.json()

    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)

    except Exception as error:
        logging.info(f"error get_models_gp3 {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"error get_models_gp3 : {error}",
        )
