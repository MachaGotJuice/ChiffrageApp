import streamlit as st
import pandas as pd
from utils import read_parameters_file

def synthese_page():
    st.title("Synthèse")

    # Load parameters and operations from file
    params_file_name = "parametres.txt"
    params, operations = read_parameters_file(params_file_name)

    # Synthèse de la page Gamme
    st.header("Synthèse de la Gamme")
    if 'operations' in st.session_state and 'num_items' in st.session_state:
        gamme_data = []
        for i in range(st.session_state.num_items):
            item_name = st.session_state.get(f"item_name_{i+1}", f"Item {i+1}")
            description = st.session_state.get(f"description_{i+1}", None)
            ref_plan = st.session_state.get(f"reference_plan_{i+1}", None)
            descriptif = st.session_state.get(f"descriptif_{i+1}", None)
            nombre_fils = st.session_state.get(f"nombre_fils_{i+1}", None)
            quantite = st.session_state.get(f"quantite_{i+1}", None)
            quantite_optionnelle = st.session_state.get(f"quantite_optionnelle_{i+1}", None)
            
            for j, op in enumerate(st.session_state.operations[i]):
                temps = operations.get(op, 0)
                dmh = temps / 3600 * 1000  # Conversion en DMH
                coeff = st.session_state.coefficients[i].get(op, None)
                gamme_data.append([item_name, description, ref_plan, descriptif, nombre_fils, quantite, quantite_optionnelle, op, temps, dmh, coeff])
        
        gamme_df = pd.DataFrame(gamme_data, columns=["Nom de l'item", "Description", "Reference Plan", "Descriptif", "Nombre de fils", "Quantité", "Quantité optionnelle", "Opération", "Temps (s)", "Temps (DMH)", "Coefficient"])
        st.table(gamme_df)
    else:
        st.write("Aucune information disponible pour la Gamme.")

    # Synthèse de la page Outillage
    st.header("Synthèse de l'Outillage")
    if 'num_moyens' in st.session_state:
        total_outillage = sum(float(st.session_state.get(f"prix_tot_{i + 1}", 0)) for i in range(st.session_state.num_moyens))
        outillage_data = []
        for i in range(st.session_state.num_moyens):
            designation = st.session_state.get(f"designation_{i+1}", None)
            fournisseur = st.session_state.get(f"fournisseur_{i+1}", None)
            ref_fournisseur = st.session_state.get(f"ref_fournisseur_{i+1}", None)
            quantite = st.session_state.get(f"quantite_{i+1}", None)
            prix_uni = st.session_state.get(f"prix_uni_{i+1}", None)
            prix_tot = st.session_state.get(f"prix_tot_{i+1}", None)
            outillage_data.append([designation, fournisseur, ref_fournisseur, quantite, prix_uni, prix_tot])
        
        outillage_df = pd.DataFrame(outillage_data, columns=["Désignation", "Fournisseur", "Référence Fournisseur", "Quantité", "Prix Uni (€)", "Prix Tot (€)"])
        st.table(outillage_df)

        st.subheader(f"Total Outillage: {total_outillage:.2f} €")
    else:
        st.write("Aucune information disponible pour l'Outillage.")

    # Synthèse de la page Offre
    st.header("Synthèse de l'Offre")
    offre_data = []
    offre_data.append(["Transport Import /export", st.session_state.get("transport_import_export", "None")])
    offre_data.append(["Outillage", f"{total_outillage:.2f} €"])
    offre_data.append(["Frais Etudes NRE/Program", st.session_state.get("frais_etudes_nre_program", "None")])
    offre_data.append(["Condition de payement", st.session_state.get("condition_paiement", "None")])
    offre_data.append(["Raw Materiel", st.session_state.get("raw_materiel", "None")])
    offre_data.append(["Test electrique", st.session_state.get("test_electrique", "None")])
    offre_data.append(["Transport", st.session_state.get("transport", "None")])
    offre_data.append(["Validité", st.session_state.get("validite", "None")])
    offre_data.append(["Packaging", st.session_state.get("packaging", "None")])

    offre_df = pd.DataFrame(offre_data, columns=["Élément", "Valeur"])
    st.table(offre_df)
