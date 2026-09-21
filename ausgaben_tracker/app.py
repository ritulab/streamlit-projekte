import streamlit as st
import pandas as pd

st.title("Ausgaben-Tracker")

if "ausgaben" not in st.session_state:
    st.session_state.ausgaben = []

with st.form("ausgaben_form", clear_on_submit=True):
    beschreibung = st.text_input("Beschreibung")
    betrag = st.number_input("Betrag (€)", min_value=0.0, step=0.5)
    kategorie = st.selectbox("Kategorie", ["Essen", "Transport", "Freizeit", "Sonstiges"])
    submit = st.form_submit_button("Hinzufügen")

if submit:
    if beschreibung.strip() == "" or betrag <= 0:
        st.error("Bitte Beschreibung und einen Betrag > 0 eingeben.")
    else:
        st.session_state.ausgaben.append(
            {"beschreibung": beschreibung, "betrag": betrag, "kategorie": kategorie}
        )
        st.rerun()

st.divider()

if not st.session_state.ausgaben:
    st.info("Noch keine Ausgaben erfasst.")
else:
    df = pd.DataFrame(st.session_state.ausgaben)

    col1, col2 = st.columns(2)
    col1.metric("Gesamtsumme", f"{df['betrag'].sum():.2f} €")
    col2.metric("Anzahl", len(df))

    st.dataframe(df)

    summen = df.groupby("kategorie")["betrag"].sum()
    st.bar_chart(summen)

    if st.button("Alle Einträge löschen"):
        st.session_state.ausgaben = []
        st.rerun()

    st.subheader("Einzelne Ausgabe löschen")
    for index, eintrag in enumerate(st.session_state.ausgaben):
        col_a, col_b = st.columns([0.8, 0.2])
        with col_a:
            st.write(f"{eintrag['beschreibung']} – {eintrag['betrag']:.2f} € ({eintrag['kategorie']})")
        with col_b:
            if st.button("❌", key=f"delete_{index}"):
                st.session_state.ausgaben.pop(index)
                st.rerun()    
                