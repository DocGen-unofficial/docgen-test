import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from microservices.fetch_repo_from_blob.src.api import router as fetch_repo_router
#from microservices.repo_downloader.endpoints.repo_download_api import router as repo_download_api
from microservices.repo_downloader.endpoints.status import router as status
#from microservices.upload_repo_on_blob.src.endpoints.endpoint_uploader import router  as endpoint_uploader

app = FastAPI(
    title="DocGen API",
    description="Web App to generate documentation with AI"
)


app.include_router(status)
#app.include_router(repo_download_api)
#app.include_router(endpoint_uploader)
app.include_router(fetch_repo_router)


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
        port=8083,
        log_level="info"
    )

    server = uvicorn.Server(server_configuration)
    server.run()