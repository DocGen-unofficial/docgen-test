import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.input_layer.status import router as status_router
from api.input_layer.repo_download_api import router as download_repository


app = FastAPI(
    title="DocGen API",
    description="Web App to generate documentation with AI"
)

app.include_router(status_router)
app.include_router(download_repository)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == '__main__':

    server_configuration = uvicorn.Config(
        app,
        host="localhost",
        port=8081,
        log_level="info"
    )

    server = uvicorn.Server(server_configuration)
    server.run()