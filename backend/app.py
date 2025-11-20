import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# App metadata
app = FastAPI()


# Run with: python app.py
if __name__ == "__main__":

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)