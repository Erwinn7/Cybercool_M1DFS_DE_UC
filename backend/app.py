import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import re

"""
stats.json : 
{    "count_scan": 0,
    "count_form_login": 0,
    "count_form_login_verified": 0}
"""

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

def verify_username(username: str) -> bool:
    try:
        user_id = int(username)
        return 18000000 < user_id < 20261000
    except ValueError:
        return False
    
def verify_password(password: str, username: Optional[str] = None) -> bool:
    if not isinstance(password, str):
        return False
    if len(password) < 10:
        return False
    if username and username.lower() in password.lower():
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[~!@\$%\^*\(\)\{\}\[\],\./]', password):
        return False
    return True

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        with open("stats.json", "r") as f:
            stats = json.load(f)
        stats["count_form_login"] += 1
        with open("stats.json", "w") as f:
            json.dump(stats, f)
        print("stats updated")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    try:
        if verify_username(username) and verify_password(password, username):
            print("tout ok")
            try:
                with open("stats.json", "r") as f:
                    stats = json.load(f)
                stats["count_form_login_verified"] += 1
                with open("stats.json", "w") as f:
                    json.dump(stats, f)
                print("stats vérifié updated")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            print("username ou mdp pas ok")
    except Exception as e:
        print("username ou mdp pas ok")
    finally:
        return {"message": "Login successful"}

@app.post("/scan")
def scan():
    try:
        with open("stats.json", "r") as f:
            stats = json.load(f)
        stats["count_scan"] += 1
        with open("stats.json", "w") as f:
            json.dump(stats, f)
        return {"message": "Scan counted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)