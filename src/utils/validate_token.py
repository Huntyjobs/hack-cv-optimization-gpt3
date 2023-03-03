from fastapi import Header, HTTPException
from settings import Settings

settings = Settings()


def validate_auth_token(x_auth_token: str = Header(...)):
    if x_auth_token != settings.HEADER_VALIDATION:
        raise HTTPException(status_code=401)
    else:
        return True
