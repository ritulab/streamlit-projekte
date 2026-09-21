import streamlit as st
import pandas as pd
import sqlite3

@st.cache_data
def load_data(query):
    conn = sqlite3.connect("Chinook_Sqlite.sqlite")
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("Music Store Dashboard")

tabelle = st.selectbox("Tabelle wählen:", ["Artist", "Album", "Customer", "Employee", "Genre", "Invoice", "InvoiceLine", "MediaType", "PlaylistTrack", "Track"])

query = f"SELECT * FROM {tabelle} LIMIT 50"
df = load_data(query)
st.dataframe(df)

st.header("Kennzahlen")

umsatz = load_data("SELECT SUM(Total) FROM Invoice").iloc[0, 0]
kunden = int(load_data("SELECT COUNT(*) FROM Customer").iloc[0, 0])
tracks = int(load_data("SELECT COUNT(*) FROM Track").iloc[0, 0])

col1, col2, col3 = st.columns(3)
col1.metric("Gesamtumsatz", f"{umsatz:.2f} $")
col2.metric("Anzahl Kunden", kunden)
col3.metric("Anzahl Tracks", tracks)

st.header("Top 10 Künstler nach Umsatz")

query_artists = """
SELECT Artist.Name AS Kuenstler,
       SUM(InvoiceLine.UnitPrice * InvoiceLine.Quantity) AS Umsatz
FROM Artist
JOIN Album ON Album.ArtistId = Artist.ArtistId
JOIN Track ON Track.AlbumId = Album.AlbumId
JOIN InvoiceLine ON InvoiceLine.TrackId = Track.TrackId
GROUP BY Artist.Name
ORDER BY Umsatz DESC
LIMIT 10
"""
df_artists = load_data(query_artists)
st.bar_chart(df_artists, x="Kuenstler", y="Umsatz")


st.header("Beliebteste Genres")

query_genres = """
SELECT Genre.Name AS Genre,
       COUNT(InvoiceLine.InvoiceLineId) AS Verkaeufe
FROM Genre
JOIN Track ON Track.GenreId = Genre.GenreId
JOIN InvoiceLine ON InvoiceLine.TrackId = Track.TrackId
GROUP BY Genre.Name
ORDER BY Verkaeufe DESC
LIMIT 5
"""
df_genres = load_data(query_genres)
st.bar_chart(df_genres, x="Genre", y="Verkaeufe")
