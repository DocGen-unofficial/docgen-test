import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.endpoints.endpoint_uploader import router as upload_router

app = FastAPI(
    title="DocGen API",
    description="Web App to generate documentation with AI"
)

app.include_router(upload_router)


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
        host="0.0.0.0",
        port=8082,
        log_level="info"
    )

    server = uvicorn.Server(server_configuration)
    server.run()
