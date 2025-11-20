import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# App metadata
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print(f"Received login attempt for user: {username}, password: {password}")
    # Ici vous pouvez ajouter votre logique d'authentification
    return {"message": "Login successful", "username": username}


# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)