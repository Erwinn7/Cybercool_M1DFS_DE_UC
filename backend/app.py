import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# App metadata
app = FastAPI()

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    print(f"Received login attempt for user: {username}, {password}")
    return {"message": "Login successful"}


# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)