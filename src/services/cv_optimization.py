import logging

from fastapi import HTTPException, status

from clients.gpt3 import create_text_gp3
from enums.instructions import Instructions


def create_text(data):
    try:
        text = create_text_gp3(
            prompt=data, instructions=Instructions.corrige_el_texto.value
        )["choices"][0]["text"]

        return {"data": text}

    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)

    except Exception as error:
        logging.info(f"update_role error {error}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"error create tex : {error}",
        )
