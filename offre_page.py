import streamlit as st

def initialize_session_state_key(key, default_value):
    """Initialize a session state key with a default value if it doesn't exist."""
    if key not in st.session_state:
        st.session_state[key] = default_value

def offre_page():
    st.title("Offre")

    # Keys for input fields in the Offre page
    transport_key = "transport_import_export"
    outillage_key = "outillage"
    frais_etudes_key = "frais_etudes"
    condition_paiement_key = "condition_paiement"
    raw_materiel_key = "raw_materiel"
    test_electrique_key = "test_electrique"
    transport_key = "transport"
    validite_key = "validite"
    packaging_key = "packaging"

    # Initialize session state for all fields
    initialize_session_state_key(transport_key, "")
    initialize_session_state_key(outillage_key, "")
    initialize_session_state_key(frais_etudes_key, "")
    initialize_session_state_key(condition_paiement_key, "10 jours par virement bancaire")
    initialize_session_state_key(raw_materiel_key, "")
    initialize_session_state_key(test_electrique_key, "")
    initialize_session_state_key(transport_key, "")
    initialize_session_state_key(validite_key, 0)
    initialize_session_state_key(packaging_key, "inclus")

    # Input fields
    st.session_state[transport_key] = st.text_input("Transport Import / Export", value=st.session_state[transport_key])
    st.session_state[outillage_key] = st.text_input("Outillage", value=st.session_state[outillage_key])
    st.session_state[frais_etudes_key] = st.text_input("Frais Etudes NRE / Program", value=st.session_state[frais_etudes_key])
    
    # Dropdown for condition de paiement
    st.session_state[condition_paiement_key] = st.selectbox("Condition de paiement", 
                                                           ["10 jours par virement bancaire", "20 jours par virement bancaire", 
                                                            "30 jours par virement bancaire", "60 jours par virement bancaire"], 
                                                           index=["10 jours par virement bancaire", 
                                                                  "20 jours par virement bancaire", 
                                                                  "30 jours par virement bancaire", 
                                                                  "60 jours par virement bancaire"].index(st.session_state[condition_paiement_key]))

    st.session_state[raw_materiel_key] = st.text_input("Raw Materiel", value=st.session_state[raw_materiel_key])
    st.session_state[test_electrique_key] = st.text_input("Test Electrique", value=st.session_state[test_electrique_key])
    st.session_state[transport_key] = st.text_input("Transport", value=st.session_state[transport_key])
    st.session_state[validite_key] = st.number_input("Validité", min_value=0, value=st.session_state[validite_key])
    
    # Dropdown for packaging
    st.session_state[packaging_key] = st.selectbox("Packaging", ["inclus", "non inclus"], 
                                                   index=["inclus", "non inclus"].index(st.session_state[packaging_key]))
