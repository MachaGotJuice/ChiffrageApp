import streamlit as st

def main_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Gestion de Projet de Chiffrage")
        st.write("")

        new_project_button = st.button("Créer un nouveau projet de chiffrage")
        open_project_button = st.button("Ouvrir un projet de chiffrage")

        if new_project_button:
            st.session_state.page = "Nouveau Projet"
        
        if open_project_button:
            st.write("Projet de chiffrage ouvert !")
