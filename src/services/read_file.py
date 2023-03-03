import logging
import typing

from fastapi import HTTPException, status
from google.cloud import documentai_v1 as document


def process_document(
    file: typing.BinaryIO,
    mime_type: str,
    project_id: str,
    location: str,
    processor_id: str,
    file_english: bool,
) -> document.Document:
    """
    It takes a file, mime_type, project_id, location, and processor_id as arguments, and returns a list of dictionaries
    containing the extracted text

    :param file: The file to be processed
    :type file: typing.BinaryIO
    :param mime_type: The MIME type of the file
    :type mime_type: str
    :param project_id: The ID of the project that owns the processor
    :type project_id: str
    :param location: The region where the Document AI API is hosted
    :type location: str
    :param processor_id: The ID of the processor to use
    :type processor_id: str
    :return: A list of dictionaries with the functions of the user
    """
    try:
        client_options = {"api_endpoint": f"{location}-documentai.googleapis.com"}
        client = document.DocumentProcessorServiceClient(client_options=client_options)

        raw_document = document.RawDocument(content=file.read(), mime_type=mime_type)
        name = client.processor_path(project_id, location, processor_id)

        request = document.ProcessRequest(
            raw_document=raw_document,
            name=name,
            skip_human_review=True,
        )
        response = client.process_document(request)

        if file_english:
            Funciones = "Functions:"
            Logros = "Achievements:"
        else:
            Funciones = "Funciones:"
            Logros = "Logros:"

        data = response.document.text.split(Funciones)
        data.pop(0)

        data_user = []

        data_user.append({f"cv_text": response.document.text})
        for index, item in enumerate(data):
            text = item.find(Logros)
            text_mod = item[0:text]
            data_user.append({f"Funciones_{index}": text_mod})

        return data_user

    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)

    except Exception as error:
        logging.info(f"error process_document {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"error process_document : {error}",
        )
