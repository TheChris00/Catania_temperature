"""
Ora abbiamo un problema: la tabella SQL è bellissima 
per te che sei l'Ingegnere, ma se la fai vedere a un 
manager o a un cliente, non ci capirà nulla. 
Loro vogliono i grafici, vogliono i cruscotti (le Dashboard).

È qui che entra in gioco Streamlit, 
la libreria Python che trasforma il tuo codice in 
un'applicazione web interattiva in pochissimi minuti.


"""


import streamlit as st
import pandas as pd
import sqlite3


# 1. Titolo e intestazione della pagina web

st.title("🌤️ Dashboard Meteo in Tempo Reale")
st.write("I dati vengono letti in diretta dal mio database SQL locale!")

# 2. Ci colleghiamo al database

connessione = sqlite3.connect("meteo_catania.db")

# 3. uniamo SQL e Pandas!

query = "SELECT data_ora, temperatura from Storico_Meteo"

dati = pd.read_sql_query(query, connessione)

connessione.close()

# 4. Mostriamo i dati sulla pagina web

st.subheader("Tabella dei Dati Grezzi")
st.dataframe(dati) # creiamo una tabella interattiva stile Excel

# 5. creiamo il grafico!

st.subheader("Andamento della temperatura")
# Diciamo a Pandas di usare la data come asse X (orizzontale) del grafico
dati.set_index('data_ora', inplace = True)
st.line_chart(dati) # Disegna un grafico a linee!