from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from tensorflow.keras.models import load_model
import numpy as np

app = FastAPI()
# Clé API WeatherAPI
api_key = "eb167a3a4951421894c110806243011"

# Configurer les options CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser uniquement React en local
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

def ask_data(localisation):
    # Ville ou coordonnées cibles (par exemple : Paris ou "48.8566,2.3522")
    loc = f"{localisation}"
    url_lieu = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={loc}"
    response = requests.get(url_lieu)
    if response.status_code == 200:
        data = response.json()
        print(f"Météo actuelle à {data['location']['name']}, {data['location']['country']}:")
        print(f" - Température : {data['current']['temp_c']}°C")
        print(f" - Humidité : {data['current']['humidity']}%")
        print(f" - Condition : {data['current']['condition']['text']}")
        return {"temp" : data['current']['temp_c'],"prep" : data['current']['humidity'],"hum" : (100-int(data['current']['precip_in']))}
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return {"temp" : 1,"prep" : 1,"hum" : 1}
    

def prediction(localisation):
    model = load_model('model_temp_hum_prep.h5')
    data = ask_data(localisation)
    nouvelle_observation = np.array([[data['temp'],data['hum'],data['prep']]])
    print(nouvelle_observation)
    probabilites = model.predict(nouvelle_observation)
    print("Probabilitées pour chaque classe:", probabilites)

    classe_predite = np.argmax(probabilites, axis=1)
    print("Classe prédite :", classe_predite)

    corespondance = {0 : 'rice', 1 : 'maize', 2 : 'jute', 3 : 'cotton', 4 : 'coconut', 5 : 'papaya', 6 : 'orange', 7 : 'apple', 8 : 'muskmelon', 9 : 'watermelon', 10 : 'grapes', 11 : 'mango', 12 : 'banana', 13 : 'pomegranate', 14 : 'lentil', 15 : 'blackgram', 16 : 'mungbean', 17 : 'mothbeans', 18 : 'pigeonpeas', 19 : 'kidneybeans', 20 : 'chickpea', 21 : 'coffee'}
    culture = corespondance[int(classe_predite[0])]
    print(f"Classe prédite: {classe_predite}/{culture}")    
    return culture

class Localisation(BaseModel):
    lieu : str

@app.post("/send-data/")
async def send_data(loc : Localisation):
    return ask_data(loc)

@app.post("/send-prediction/")
async def send_prediction(loc: Localisation):
    culture = prediction(loc)
    return {"culture" : f"{culture}"}

