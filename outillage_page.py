import streamlit as st

def initialize_session_state_key(key, default_value):
    """Initialize a session state key with a default value if it doesn't exist."""
    if key not in st.session_state:
        st.session_state[key] = default_value
        print(key +"NOT IN")
    else:
        print(key + "in")

def calculate_prix_total(quantite, prix_unitaire):
    """Calculate the total price based on quantity and unit price."""
    return quantite * prix_unitaire

def outillage_page():
    st.title("Outillage")

    # Ensure num_moyens (number of moyens) is initialized in session state
    if 'num_moyens' not in st.session_state:
        st.session_state.num_moyens = 1

    # Iterate over each "moyen" and ensure keys are initialized
    for i in range(st.session_state.num_moyens):
        designation_key = f"designation_{i+1}"
        fournisseur_key = f"fournisseur_{i+1}"
        ref_fournisseur_key = f"ref_fournisseur_{i+1}"
        quantite_key = f"quantite_{i+1}"
        prix_uni_key = f"prix_uni_{i+1}"
        prix_tot_key = f"prix_tot_{i+1}"
        photo_key = f"photo_{i+1}"

        # Initialize keys with default values if they don't exist
        initialize_session_state_key(designation_key, "")
        initialize_session_state_key(fournisseur_key, "")
        initialize_session_state_key(ref_fournisseur_key, "")
        initialize_session_state_key(quantite_key, 0)
        initialize_session_state_key(prix_uni_key, 0.0)
        initialize_session_state_key(prix_tot_key, 0.0)
        initialize_session_state_key(photo_key, None)

        with st.expander(f"Moyen {i+1}"):
            st.session_state[designation_key] = st.text_input("Désignation", value=st.session_state[designation_key], key=f"designation_blank{i+1}")
            st.session_state[fournisseur_key] = st.text_input("Fournisseur", value=st.session_state[fournisseur_key], key=f"fournisseur_blank{i+1}")
            st.session_state[ref_fournisseur_key] = st.text_input("Référence Fournisseur", value=st.session_state[ref_fournisseur_key], key=f"ref_fournisseur_blank{i+1}")
            
            # Input fields for Quantité and Prix Unitaire
            st.session_state[quantite_key] = st.number_input("Quantité", min_value=0, value=st.session_state[quantite_key], key=f"quantite_blank{i+1}")
            st.session_state[prix_uni_key] = st.number_input("Prix Unitaire (€)", min_value=0.0, value=st.session_state[prix_uni_key], key=f"prix_uni_blank{i+1}")
            
            # Dynamically calculate Prix Total
            st.session_state[prix_tot_key] = calculate_prix_total(st.session_state[quantite_key], st.session_state[prix_uni_key])
            st.number_input("Prix Total (€)", value=st.session_state[prix_tot_key], disabled=True, key=f"prix_total{i+1}" )

            # Upload and display a photo for the "Moyen"
            uploaded_photo = st.file_uploader("Photo du moyen", key=f"photo_blank{i+1}")
            if uploaded_photo is not None:
                st.session_state[photo_key] = uploaded_photo
            if st.session_state[photo_key] is not None:
                st.image(st.session_state[photo_key], caption=f"Photo du Moyen {i+1}", use_column_width=True)

    # Button to add a new "moyen"
    if st.button("+ Ajouter un moyen"):
        st.session_state.num_moyens += 1
        st.session_state[f"designation_{st.session_state.num_moyens}"] = ""
        st.session_state[f"fournisseur_{st.session_state.num_moyens}"] = ""
        st.session_state[f"ref_fournisseur_{st.session_state.num_moyens}"] = ""
        st.session_state[f"quantite_{st.session_state.num_moyens}"] = 0
        st.session_state[f"prix_uni_{st.session_state.num_moyens}"] = 0.0
        st.session_state[f"prix_tot_{st.session_state.num_moyens}"] = 0.0
        st.session_state[f"photo_{st.session_state.num_moyens}"] = None
