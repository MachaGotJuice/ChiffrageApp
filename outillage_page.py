import streamlit as st

def outillage_page():
    st.title("Outillage")
    
    # Initialiser la liste des moyens si elle n'existe pas déjà
    if 'num_moyens' not in st.session_state:
        st.session_state.num_moyens = 1  # Commence avec un moyen

    # Boucle pour afficher chaque moyen
    for i in range(st.session_state.num_moyens):
        with st.expander(f"Moyen {i + 1}"):
            # Saisie des informations pour chaque moyen
            designation = st.text_input("Désignation", key=f"designation_{i + 1}")
            fournisseur = st.text_input("Fournisseur", key=f"fournisseur_{i + 1}")
            ref_fournisseur = st.text_input("Référence Fournisseur", key=f"ref_fournisseur_{i + 1}")
            quantite = st.number_input("Quantité", min_value=0, step=1, key=f"quantite_{i + 1}")
            prix_uni = st.number_input("Prix Uni (euros)", min_value=0.0, step=0.01, format="%.2f", key=f"prix_uni_{i + 1}")
            
            # Calcul du prix total
            prix_tot = quantite * prix_uni
            st.text_input("Prix Tot (euros)", value=f"{prix_tot:.2f}", disabled=True, key=f"prix_tot_{i + 1}")

            # Option pour insérer une photo
            uploaded_file = st.file_uploader("Choisissez une image", type=["png", "jpg", "jpeg"], key=f"photo_{i + 1}")
            
            if uploaded_file is not None:
                st.image(uploaded_file, use_column_width=True)

    # Bouton pour ajouter un nouveau moyen
    if st.button("Ajouter un moyen"):
        st.session_state.num_moyens += 1  # Incrémente le nombre de moyens

# Assurez-vous que cette fonction est appelée dans votre app.py
