import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.base_routers import api_v1_router
from app.settings import settings, EnvironmentEnum
from app.systems.ingestion.dpu_storage.ingest_egress_lifespan import ingress_on_startup, egress_on_shutdown


# -----
# Lifespan manages code executed before startup and after shutdown
# -----
@asynccontextmanager
async def lifespan(app: FastAPI):
    # When enabled we can fill the duckdb instance with a copy saved on azure blob storage
    await ingress_on_startup()

    # -----
    # Yielding will start the fastapi application
    yield
    # After yielding, so a shutdown (or crash?) we arrive here
    # -----

    # We can connect to the azure blob storage for dpu and offload all duckdb files
    await egress_on_shutdown()

# -----
# List of applied middleware
# From left to right ( imagine as .pop() )
# -----
middleware = []

# -----
# Cors
# -----
allowed_origins = [
    "https://ingeniumua.be",
    "https://admin.ingeniumua.be",
    "https://dashboard.ingeniumua.be",
    "https://www.ingeniumua.be",
    "https://accounts.google.com",
]
if settings.running_environment.value == EnvironmentEnum.staging.value:
    allowed_origins += [
        "https://dev.ingeniumua.be",
        "https://staging.ingeniumua.be"
    ]
if settings.running_environment.value == EnvironmentEnum.local.value:
    allowed_origins += [
        "http://localhost:4200",
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:8000"
    ]


app = FastAPI(title="IngeniumUAHub Data API",
              docs_url="/docs",
              terms_of_service="/tos",
              contact={"email": "info@ingeniumua.be"},
              licence_info={"MIT License Copyright (c) 2023 IngeniumUA VZW"},
              middleware=middleware,
              dependencies=[]
              )
app.include_router(api_v1_router)
# app.include_router(static_pages_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----
# Exception interceptors
# https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers
# ----
# TODO
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return validation_intercept(request=request, exception=exc)


@app.get("/")
async def root():
    return {"message": "Hey! Dit is onze API, jij bent verdwaald geraakt :)"}

@app.get("/health")
async def health_check():
    return True


if __name__ == "__main__":
    reload = os.getenv("environment") == "local"  # If running in local environment, reload the server on changes
    try:
        uvicorn.run("main:app", host="0.0.0.0", reload=reload, port=8000)
    except Exception as e:
        print(f"Initializing app failed: {e}")