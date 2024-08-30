import streamlit as st

def offre_page():
    st.title("Offre")

    # Récupérer la somme des prix totaux des moyens depuis la page Outillage
    if 'num_moyens' in st.session_state:
        total_outillage = sum(float(st.session_state.get(f"prix_tot_{i + 1}", 0)) for i in range(st.session_state.num_moyens))
    else:
        total_outillage = 0.0

    # Saisie des informations et stockage dans st.session_state
    st.session_state.transport_import_export = st.text_input("Transport Import /export", value=st.session_state.get("transport_import_export", ""))
    st.session_state.outillage = st.text_input("Outillage", value=f"{total_outillage:.2f} €", disabled=True)
    st.session_state.frais_etudes_nre_program = st.text_input("Frais Etudes NRE/Program", value=st.session_state.get("frais_etudes_nre_program", ""))
    
    # Liste déroulante pour condition de paiement
    condition_paiement_options = ["10 jours par virement bancaire", "20 jours par virement bancaire", "30 jours par virement bancaire", "60 jours par virement bancaire"]
    st.session_state.condition_paiement = st.selectbox("Condition de payement", options=condition_paiement_options, index=condition_paiement_options.index(st.session_state.get("condition_paiement", "30 jours par virement bancaire")))

    st.session_state.raw_materiel = st.text_input("Raw Materiel", value=st.session_state.get("raw_materiel", ""))
    st.session_state.test_electrique = st.text_input("Test electrique", value=st.session_state.get("test_electrique", ""))
    st.session_state.transport = st.text_input("Transport", value=st.session_state.get("transport", ""))
    
    # Champ pour entrer la validité (en jours)
    st.session_state.validite = st.number_input("Validité (jours)", min_value=0, step=1, value=st.session_state.get("validite", 0))

    # Liste déroulante pour packaging
    packaging_options = ["Inclus", "Non inclus"]
    st.session_state.packaging = st.selectbox("Packaging", options=packaging_options, index=packaging_options.index(st.session_state.get("packaging", "Inclus")))

    # Bouton pour enregistrer les informations
    if st.button("Enregistrer"):
        st.success("Les informations de l'offre ont été enregistrées.")
        # Logique pour sauvegarder les données peut être ajoutée ici

# Assurez-vous que cette fonction est appelée dans votre app.py
