from fastapi import FastAPI
import pickle 
import pandas as pd
from datetime import datetime

# 1. Inizializziamo l'applicazione web API

app = FastAPI(title= "Meteo Catania AI API")

# 2. "Scongeliamo" il modello all'avvio del server

with open("modello_meteo.pkl", "rb") as file:
    modello = pickle.load(file)

# 3. Creiamo un "Endpoint" (una porta d'accesso web)

@app.get("/prevedi")
def prevedi_temperatura():
    # Prendiamo l'ora di questo esatto momento e la trasformiamo in numero
    ora_attuale = pd.Timestamp.timestamp(pd.to_datetime(datetime.now()))

    # Creiamo un "finto" dato futuro (es. tra 1 ora, aggiungendo 3600 secondi)
    ora_futura = ora_attuale + 3600

    # Chiediamo al modello AI di fare la previsione!
    X_futura = pd.DataFrame({'tempo_numerico': [ora_futura]})
    previsione = modello.predict(X_futura)[0]

    # L'API risponde sempre in formato JSON (Dizionario)
    return{

        "messaggio": "Previsione per la prossima ora a Catania",
        "temperatura_stimata": round(previsione, 2)
    }