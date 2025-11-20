import datetime
import json
import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates  
import uvicorn


# App metadata
app = FastAPI()


LOG_FILE = "visits.json"   # database
COOKIE_QR = "visited_qr"
COOKIE_DIRECT = "visited_direct"

# Templates directory
templates = Jinja2Templates(directory="frontend")


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/login")
async def show_login(request: Request):
    """
    Affiche le formulaire de login.
    Utiliser ?source=direct pour marquer la visite comme 'direct', sinon elle sera 'qr'.
    """
    response = templates.TemplateResponse("index.html", {"request": request})
    # Marque la visite côté client (valeur simple, durée 1h)
    return response

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print(f"Received login attempt for user: {username}, password: {password}")
    # Ici vous pouvez ajouter votre logique d'authentification

    log_visit()
    return {"message": "Login successful", "username": username}


# -----------------------------
#  Load / Save JSON database
# -----------------------------

def load_db():
    if not os.path.exists(LOG_FILE):
        empty = {"loginQR": [], "loginDirect": []}
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
        db["loginQR"].append(timestamp)
    elif source == "direct":
        db["loginDirect"].append(timestamp)

    save_db(db)


# -----------------------------
#  affichage des stats
# -----------------------------


def read_stats():
    with open("stats.json", "r") as f:
        return json.load(f)

@app.get("/stats")
def stats(request: Request):
    data = read_stats()
    return templates.TemplateResponse("stats.html", {"request": request, "connections": data})



# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)