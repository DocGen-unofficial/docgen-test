from microservices.transforming_pipeline.components.python_to_text_conversion.filtering.source.cleaner_comments import Filtering
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.filtering_api import router as filter

app = FastAPI(
    title="DocGen API",
    description="Web App to generate documentation with AI"
)

app.include_router(filter)

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

    #C:/WorkingDirectory/AIDocGen/microservices/transforming_pipeline/python_to_text_conversion/filtering/tests/robertoparodo-unicassistant_part_0.parquet
