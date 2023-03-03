import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import gpt3_text, cv_file
from settings import Settings

settings = Settings()

app = FastAPI(
    title="CV optimization API",
    description="",
    version="0.0.1",
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(gpt3_text.router)
app.include_router(cv_file.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
