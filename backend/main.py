from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(title="Matrix Neural Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}
