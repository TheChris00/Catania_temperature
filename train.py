import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

print("🔄 Inizio estrazione dati e addestramento del modello...")

# 1. ESTRAZIONE (dal tuo salvadanaio)

connessione = sqlite3.connect("meteo_catania.db")
dati = pd.read_sql_query("SELECT data_ora, temperatura FROM Storico_Meteo", connessione)
connessione.close()

#2. PREPARAZIONE DEI DATI (Feature Engineering)
# Problema: L'algoritmo è una formula matematica, "mangia" solo numeri. 
# Non capisce un testo come "2026-02-25 14:30:00".
# Soluzione: Trasformiamo la data in un numero (i secondi trascorsi dal 1970, chiamato Timestamp).

dati['data_ora'] = pd.to_datetime(dati['data_ora'])
dati['tempo_numerico'] = dati['data_ora']

# Definiamo cosa usare per prevedere (X) e cosa vogliamo indovinare (y

X = dati[['tempo_numerico']] # La nostra X è il tempo che scorre
y = dati['temperatura'] # La nostra Y è la temperatura

# 3. Addestramento

modello = LinearRegression()
modello.fit(X, y) # Qui l'algoritmo "studia" come la temperatura è cambiata nel tempo

# 4. Salvataggio
# Non vogliamo riaddestrare il modello ogni volta che ci serve una previsione.
# Lo "congeliamo" in un file .pkl (pickle) per poterlo riutilizzare ovunque.

with open("modello_meteo.pkl", "wb") as file:
    pickle.dump(modello, file)

print("✅ Modello addestrato e salvato con successo nel file 'modello_meteo.pkl'!")