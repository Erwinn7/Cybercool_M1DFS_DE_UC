import datetime
import json
import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# App metadata
app = FastAPI()


LOG_FILE = "login_times.json"

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

    log_login_time()
    return {"message": "Login successful", "username": username}


def log_login_time():
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()

    # If file doesn't exist, create it
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump({"logins": []}, f, indent=4)

    # Load existing data
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    data["logins"].append(timestamp)

    # Write updated data
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)