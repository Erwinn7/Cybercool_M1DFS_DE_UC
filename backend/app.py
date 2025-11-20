import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

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

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        if (int(username) > 18000000) and (int(username) < 20261000):
            print("username ok")
            try:
                with open("stats.json", "r") as f:
                    stats = json.load(f)
                stats["count_form_login"] += 1
                with open("stats.json", "w") as f:
                    json.dump(stats, f)
                print("stats updated")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            print("username pas ok")
    except Exception as e:
        print("username pas ok")
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