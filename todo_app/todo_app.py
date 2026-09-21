import streamlit as st

st.title("Meine To-Do App")

if "todos" not in st.session_state:
    st.session_state.todos = []

with st.form(key="add_form", clear_on_submit=True):
    neue_aufgabe = st.text_input("Neue Aufgabe:")
    submit = st.form_submit_button("Hinzufügen")

if submit and neue_aufgabe:
    st.session_state.todos.append(neue_aufgabe)
    st.rerun()

st.divider()

if not st.session_state.todos:
    st.info("Noch keine Aufgaben. Füge oben deine erste Aufgabe hinzu.")
else:
    for index, aufgabe in enumerate(st.session_state.todos):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.write(aufgabe)
        with col2:
            if st.button("❌", key=f"delete_{index}"):
                st.session_state.todos.pop(index)
                st.rerun()