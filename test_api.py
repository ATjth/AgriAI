from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

def Api_meteo(localisation):
    valeur = {1 : [25, 20, 30], 2 : [30, 70, 20], 3 : [20, 80, 60]}
    choix = random.randint(0, 4)
    temp, hum, lum = valeur[choix][0], valeur[choix][1], valeur[choix][2]
    return temp, hum, lum

def model_prediction(localisation):
    print(localisation)
    return 'riz'

class Localisation(BaseModel):
    lieu : str

@app.post("/send-data/")
async def send_data(loc : Localisation):
    temp, hum, lum = 25, 35, 60
    return {"temp": f"{temp}", "hum" : f"{hum}", "lum" : f"{lum}"}

@app.post("/send-prediction/")
async def send_prediction(loc: Localisation):
    culture = model_prediction(loc)
    return {"culture" : f"{culture}"}

# Configurer les options CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser uniquement React en local
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

class Info(BaseModel):
    nom : str
    age : int

@app.post("/get-info/")
async def get_info(user_info: Info):
    return {"message" : f"nom: {user_info.nom} age: {user_info.age}"}

@app.get("/get-untruc/")
async def get_untruc():
    return {"message" : "Salut tu es content?"}
