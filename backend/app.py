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

# Chemin absolu vers le fichier de données
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Remonte de 2 niveaux (backend -> racine)
LOG_FILE = os.path.join(BASE_DIR, "data", "visits.json")   # database

# Cookies pour éviter de compter plusieurs fois la même visite
COOKIE_QR = "visited_qr"
COOKIE_DIRECT = "visited_direct"

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/qr")
async def login_qr(username: str = Form(...), password: str = Form(...)):
    print(f"Received QR login attempt for user: {username}, password: {password}")
    # Ici vous pouvez ajouter votre logique d'authentification

    log_login("qr")
    return {"message": "Login successful", "username": username}

@app.post("/login/direct")
async def login_direct(username: str = Form(...), password: str = Form(...)):
    print(f"Received direct login attempt for user: {username}, password: {password}")
    # Ici vous pouvez ajouter votre logique d'authentification

    log_login("direct")
    return {"message": "Login successful", "username": username}


# -----------------------------
#  Load / Save JSON database
# -----------------------------

def load_db():
    if not os.path.exists(LOG_FILE):
        empty = {
            "visitsQR": [],
            "visitsDirect": [],
            "loginQR": [],
            "loginDirect": []
        }
        with open(LOG_FILE, "w") as f:
            json.dump(empty, f, indent=4)
        return empty

    with open(LOG_FILE, "r") as f:
        return json.load(f)
    
def save_db(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)    

# -----------------------------
#  Fonctions pour log les visites
# -----------------------------

def log_login_time():
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()

    # Si le fichier n'existe pas, le créer
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

def log_visit(source: str = 'qr'): # Par défaut QR
    """
    source = "qr" or "direct"
    """
    db = load_db()

    timestamp = datetime.datetime.now(datetime.UTC).isoformat()

    if source == "qr":
        db["visitsQR"].append(timestamp)
    elif source == "direct":
        db["visitsDirect"].append(timestamp)

    save_db(db)

def log_login(source: str):
    """
    source: "qr" or "direct"
    """
    db = load_db()
    now = datetime.datetime.now(datetime.UTC).isoformat()

    if source == "qr":
        db["loginQR"].append(now)
    else:
        db["loginDirect"].append(now)

    save_db(db)


# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)