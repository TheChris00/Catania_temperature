"""

1. Data Ingestion (Estrazione Dati)

Cosa fare: Scrivi uno script Python che ogni giorno si collega 
a un'API gratuita (come Open-Meteo o OpenAQ) per scaricare 
i dati sull'inquinamento o sul meteo della tua città.

Le skill usate: Python (libreria requests), manipolazione dati con pandas.

Il tocco da Ingegnere: Lo script non stampa 
i dati a schermo, ma usa SQLAlchemy (o sqlite3) 
per salvarli in un database relazionale locale 
(SQLite va benissimo per iniziare).


"""

import requests 
import sqlite3
import pandas
from datetime import datetime

# -- PARTE 1: L'API --#
    # 1. definiamo le cordinate di Catania e l'indirizo dell'API

url = "https://api.open-meteo.com/v1/forecast?latitude=37.50&longitude=15.09&current_weather=true"

    # 2. Python fa una "chiamata" a quell'indirizzo internet

risposta = requests.get(url)

    # 3. Trasformiamo la risposta del sito in un formato leggibile da Python (JSON)

dati = risposta.json()

    # 4. Navighiamo dentro i dati per estrarre SOLO la temperatura

temperatura_attuale = dati["current_weather"]["temperature"]

#Il testo scaricato è un po' caotico. Il comando .json() lo riordina 
# trasformandolo in un Dizionario Python. 
# Immaginalo come una cassettiera con tante etichette.

print(f"Ciao! In questo momento a Catania ci sono {temperatura_attuale} °C.")

#Mostriamo il numero finale a noi stessi. La lettera f prima delle virgolette ci permette 
#di infilare la variabile temperatura_attuale direttamente dentro la frase.


# --adesso importiamo datatime, ci serve anche l'orario esatto in cui scarichiamo il dato! --#



orario_attuale = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"scaricato: {temperatura_attuale} °C alle {orario_attuale}")


# -- PARTE 2: Il DATABASE --#

# 1. Ci colleghiamo al database (se il file non esiste, Python lo crea da solo!)

connessione = sqlite3.connect("meteo_catania.db")
cursore = connessione.cursor()  # Il cursore è la "penna" che scrive nel database

cursore.execute("""

create table If not exists Storico_Meteo(

    id integer primary key autoincrement,
    data_ora TEXT,
    temperatura REAL
)""")

# 3. Inseriamo la riga di oggi. I punti interrogativi (?) ci proteggono dagli hacker (SQL Injection)


cursore.execute("""
    INSERT INTO Storico_Meteo (data_ora, temperatura)
    VALUES (?, ?)
    """, (orario_attuale, temperatura_attuale))


# 4. Salviamo (Commit) e chiudiamo la connessione

connessione.commit()
connessione.close()

print("Dato salvato con successo nel database in modo permanente!")