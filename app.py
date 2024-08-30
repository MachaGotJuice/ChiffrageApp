import streamlit as st
from main_page import main_page
from new_project_page import new_project_page
from gamme_page import gamme_page
from outillage_page import outillage_page
from offre_page import offre_page
from synthese_page import synthese_page  # Importer la page Synthèse



# Initialiser l'état de la page
if 'page' not in st.session_state:
    st.session_state.page = "Main"

# Afficher le menu de navigation seulement pour certaines pages
if st.session_state.page not in ["Main", "Nouveau Projet"]:
    # Ajouter un menu latéral pour la navigation entre les pages
    st.sidebar.title("Menu de Navigation")
    st.session_state.page = st.sidebar.radio(
        "Navigation",
        ["Gamme", "Outillage", "Offre", "Synthèse"]  # Ajouter Synthèse au menu
    )


# Rendre la page appropriée
if st.session_state.page == "Main":
    main_page()
elif st.session_state.page == "Nouveau Projet":
    new_project_page()
elif st.session_state.page == "Gamme":
    gamme_page()
elif st.session_state.page == "Outillage":
    outillage_page()
elif st.session_state.page == "Offre":
    offre_page()
elif st.session_state.page == "Synthèse":
    synthese_page()
