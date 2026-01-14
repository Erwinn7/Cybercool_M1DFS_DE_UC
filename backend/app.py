import datetime
import json
import os
import random
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import re

"""
stats.json : 
{    
    "count_scan": 0,
    "count_form_login": 0,
    "count_form_login_verified": 0
}

visits.json :
{
    "loginTime": [
    ],
    "scanTimeQr": [
    ],
    "scanTimeUrl": [
    ]
}
"""

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

def verify_username(username: str) -> bool:
    try:
        user_id = int(username)
        return 18000000 < user_id < 20271000
    except:
        return False
    
LOG_FILE = "visits.json"

def load_db():
    if not os.path.exists(LOG_FILE):
        empty = {"loginTime": [], "loginTimeVerified": []}
        with open(LOG_FILE, "w") as f:
            json.dump(empty, f, indent=4)
        return empty

    with open(LOG_FILE, "r") as f:
        return json.load(f)
    
def save_db(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def login_time():
    """
    Enregistre le timestamp de chaque tentative de connexion
    """
    db = load_db()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.setdefault("loginTime", []).append(timestamp)
    save_db(db)

def login_time_verified():
    """
    Enregistre le timestamp des connexions avec username au bon format
    """
    db = load_db()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.setdefault("loginTimeVerified", []).append(timestamp)
    save_db(db)

# Fonction modulaire pour incrémenter un compteur dans un JSON
def increment_json_counter(filepath: str, key: str, amount: int = 1):
    try:
        if not os.path.exists(filepath):
            # créer un fichier vide si nécessaire
            with open(filepath, "w") as f:
                json.dump({}, f)
        with open(filepath, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = {}
        data[key] = data.get(key, 0) + amount
        with open(filepath, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

@app.post("/login")
async def login(username: str = Form(...)):
    try:
        increment_json_counter("stats.json", "count_form_login", 1)
        login_time()  # Enregistre toutes les tentatives
    except Exception:
        pass
    
    if verify_username(username):
        print("Login verified")
        login_time_verified()  # Enregistre les connexions au bon format
        try:
            increment_json_counter("stats.json", "count_form_login_verified", 1)
        except Exception:
            pass
    else:
        raise HTTPException(status_code=400, detail="Login not verified")
    return HTTPException(status_code=200, detail="Login verified")

@app.post("/scan")
async def scan(request: Request, support: str = Form(None)):
    try:
        # Support peut venir soit en JSON (application/json) soit en form-data
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            body = await request.json()
            support_val: str = body.get("support")
        else:
            support_val: str = support

        with open("visits.json", "r") as f:
            visits_data = json.load(f)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if support_val.lower() == "qrcode":
            visits_data.setdefault("scanTimeQr", []).append(timestamp)
        else:
            visits_data.setdefault("scanTimeUrl", []).append(timestamp)
        with open("visits.json", "w") as f:
            json.dump(visits_data, f, indent=4)
            
    except Exception:
        pass

@app.get("/stats")
async def stats():
    try:
        with open("stats.json", "r") as f:
            dataStats = json.load(f)
        with open("visits.json", 'r') as f:
            dataVisits = json.load(f)
        return {
            "dataStats": dataStats,
            "dataVisits": dataVisits
        }
    except Exception:
        pass
    

# python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)