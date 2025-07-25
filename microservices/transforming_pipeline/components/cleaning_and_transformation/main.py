import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.api import router as text_cleaning_router

app = FastAPI(
    title="Text Cleaning API",
    description="Web App to clean text files from parquet for chunking and embedding"
)

app.include_router(text_cleaning_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':

    server_configuration = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8084,
        log_level="info"
    )


    server = uvicorn.Server(server_configuration)
    server.run()