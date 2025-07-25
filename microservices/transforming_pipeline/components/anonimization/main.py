import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints... import router as ...
from endpoints.... import router as ...

app = FastAPI(
    title="DocGen API",
    description="Web App to generate documentation with AI"
)

app.include_router(...)
app.include_router(...)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == '__main__':
    """
    Main entry point for running the DocGen API server.
    
    Configures and starts the uvicorn server on host 0.0.0.0:8084
    with info level logging.
    """
    server_configuration = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8084,
        log_level="info"
    )

    server = uvicorn.Server(server_configuration)
    server.run()