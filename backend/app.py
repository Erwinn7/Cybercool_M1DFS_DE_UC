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
    
    # Validation du username ET du password
    success = validate_credentials(username, password)
    
    # Logger la tentative (réussie ou échouée)
    log_login_attempt("qr", username, success)
    
    # Retourner toujours un succès pour la page de test
    return {"message": "Login successful", "username": username}

@app.post("/login/direct")
async def login_direct(username: str = Form(...), password: str = Form(...)):
    print(f"Received direct login attempt for user: {username}, password: {password}")
    
    # Validation du username ET du password
    success = validate_credentials(username, password)
    
    # Logger la tentative (réussie ou échouée)
    log_login_attempt("direct", username, success)
    
    # Retourner toujours un succès pour la page de test
    return {"message": "Login successful", "username": username}


# -----------------------------
#  Load / Save JSON database
# -----------------------------

def load_db():
    if not os.path.exists(LOG_FILE):
        empty = {
            "visitsQR": [],
            "visitsDirect": [],
            "loginQRValid": [],
            "loginQRInvalid": [],
            "loginDirectValid": [],
            "loginDirectInvalid": []
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

def validate_username(username: str) -> bool:
    """
    Valide que le username est numérique et dans la plage [19810000, 20300000]
    """
    try:
        user_id = int(username)
        return 19810000 <= user_id <= 20300000
    except ValueError:
        return False

def validate_password(password: str, username: str) -> bool:
    """
    Valide les critères de complexité du mot de passe :
    - Au moins 10 caractères
    - Au moins 1 majuscule (A-Z)
    - Au moins 1 minuscule (a-z)
    - Au moins 1 chiffre (0-9)
    - Au moins 1 caractère spécial (~!@$%^*(){}[],./) 
    - Ne pas contenir le login de l'utilisateur
    """
    import re
    
    if len(password) < 10:
        return False
        
    if not re.search(r'[A-Z]', password):  # Au moins 1 majuscule
        return False
        
    if not re.search(r'[a-z]', password):  # Au moins 1 minuscule
        return False
        
    if not re.search(r'[0-9]', password):  # Au moins 1 chiffre
        return False
        
    if not re.search(r'[~!@$%^*(){}\[\],./]', password):  # Au moins 1 caractère spécial
        return False
        
    if username.lower() in password.lower():  # Ne pas contenir le login
        return False
        
    return True

def validate_credentials(username: str, password: str) -> bool:
    """
    Valide les identifiants complets (username ET password)
    """
    return validate_username(username) and validate_password(password, username)

def log_login_attempt(source: str, username: str, success: bool):
    """
    Log une tentative de login (réussie ou échouée) - SANS stocker le username
    source: "qr" or "direct"
    username: utilisé seulement pour validation, pas stocké
    success: True si réussi, False si échoué
    """
    db = load_db()
    now = datetime.datetime.now(datetime.UTC).isoformat()
    
    # Stocker seulement le timestamp selon source et résultat
    if source == "qr":
        if success:
            db["loginQRValid"].append(now)
        else:
            db["loginQRInvalid"].append(now)
    else:  # direct
        if success:
            db["loginDirectValid"].append(now)
        else:
            db["loginDirectInvalid"].append(now)
    
    save_db(db)

# -----------------------------
#  API pour récupérer les statistiques
# -----------------------------

@app.get("/stats")
async def get_stats():
    """
    Retourne les statistiques de connexion (sans données personnelles)
    """
    db = load_db()
    
    return {
        "visits": {
            "qr": len(db.get("visitsQR", [])),
            "direct": len(db.get("visitsDirect", []))
        },
        "logins": {
            "qr_valid": len(db.get("loginQRValid", [])),
            "qr_invalid": len(db.get("loginQRInvalid", [])),
            "direct_valid": len(db.get("loginDirectValid", [])),
            "direct_invalid": len(db.get("loginDirectInvalid", []))
        }
    }

@app.post("/test-validation")
async def test_validation(username: str = Form(...), password: str = Form(...)):
    """
    API de test pour vérifier la validation des identifiants (pour debugging)
    """
    username_valid = validate_username(username)
    password_valid = validate_password(password, username)
    
    return {
        "username": username,
        "username_valid": username_valid,
        "password_valid": password_valid,
        "overall_valid": username_valid and password_valid,
        "password_criteria": {
            "length_ok": len(password) >= 10,
            "has_uppercase": bool(__import__('re').search(r'[A-Z]', password)),
            "has_lowercase": bool(__import__('re').search(r'[a-z]', password)),
            "has_digit": bool(__import__('re').search(r'[0-9]', password)),
            "has_special": bool(__import__('re').search(r'[~!@$%^*(){}\\[\\],./]', password)),
            "no_username": username.lower() not in password.lower()
        }
    }


# Run with: python app.py
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)