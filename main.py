"""
This module contains the main configurations for FastAPI to run.
"""
import pandas as pd
from fastapi import FastAPI
from route.api import router
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
 
PREFIX_V1 = "/challenge_2"
TAGS_METADATA = [
    {"name": "challenge2", "description": """resize, store & retrieve imagea"""}
]
 
app = FastAPI(
    title="Challenge2 Application",
    openapi_tags=TAGS_METADATA,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.include_router(router, prefix=PREFIX_V1)
 
 
if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=False
    )
