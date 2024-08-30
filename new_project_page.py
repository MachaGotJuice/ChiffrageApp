import streamlit as st
import os
import tempfile

def new_project_page():
    st.title("Nouveau Projet")
    st.write("Bienvenue sur la page de création d'un nouveau projet de chiffrage.")
    
    project_name = st.text_input("Nom du projet")
    client_name = st.text_input("Nom du client")
    urgency = st.text_input("Urgence")
    
    pursue_button = st.button("Poursuivre")

    if pursue_button:
        if project_name and client_name and urgency:
            temp_dir = os.path.join(tempfile.gettempdir(), project_name)
            os.makedirs(temp_dir, exist_ok=True)

            file_path = os.path.join(temp_dir, f"{project_name}.txt")
            with open(file_path, "w", encoding="utf-8") as temp_file:
                temp_file.write(f"Nom du projet: {project_name}\n")
                temp_file.write(f"Nom du client: {client_name}\n")
                temp_file.write(f"Urgence: {urgency}\n")
            
            st.session_state.project_name = project_name
            st.session_state.temp_file_path = file_path
            
            st.session_state.page = "Gamme"
        else:
            st.error("Veuillez remplir toutes les informations.")

    if st.button("Retour à la page principale"):
        st.session_state.page = "Main"
