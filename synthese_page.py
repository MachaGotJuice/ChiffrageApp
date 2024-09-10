import streamlit as st
import pandas as pd
from utils import read_parameters, calculate_prix_unitaire, calculate_total_time, calculate_time_per_wire

def synthese_page():
    st.title("Synthèse")

    # Load operations from parametres.py using the utility function
    operations_times = read_parameters()

    # Synthèse de la page Gamme
    st.header("Synthèse de la Gamme")
    if 'operations' in st.session_state and 'num_items' in st.session_state:
        gamme_data = []
        for i in range(st.session_state.num_items):
            item_name = st.session_state.get(f"item_name_{i+1}", f"Item {i+1}")
            ref_plan = st.session_state.get(f"reference_plan_{i+1}", "None")
            descriptif = st.session_state.get(f"descriptif_{i+1}", "None")
            quantite = st.session_state.get(f"quantite_{i+1}", 0)
            quantite_optionnelle = st.session_state.get(f"quantite_optionnelle_{i+1}", 0)

            # Calculate the sum of (coefficient * temps) for this item
            sum_of_temps_coeff = sum(
                operations_times.get(op, 0) * st.session_state.coefficients[i].get(op, 1.0)
                for op in st.session_state.operations[i]
            )

            # Retrieve necessary fields for total time calculation
            correction_difficulte = st.session_state.get(f"correction_difficulte_{i+1}", 20.0)
            setup_time = st.session_state.get(f"setup_time_{i+1}", 2.0)
            setup_quantity = st.session_state.get(f"setup_quantity_{i+1}", 10000)

            # Calculate total time and prix unitaire (labor cost)
            total_time = calculate_total_time(sum_of_temps_coeff, correction_difficulte, setup_time, setup_quantity)
            taux_horaire = 50  # Example hourly rate in euros
            prix_unitaire = calculate_prix_unitaire(total_time, taux_horaire)

            # Append the necessary information to the list
            gamme_data.append([
                item_name, ref_plan, descriptif, quantite, quantite_optionnelle, f"{prix_unitaire:.2f} €", "None"  # RM consommable to be filled later
            ])

        # Create a DataFrame to display the data
        gamme_df = pd.DataFrame(gamme_data, columns=[
            "Nom de l'item", "Reference Plan", "Descriptif", "Quantité", "Quantité optionnelle", "Cout de la main d'oeuvre", "RM consommable"
        ])
        st.table(gamme_df)
    else:
        st.write("Aucune information disponible pour la Gamme.")

    # Synthèse de la page Outillage
    st.header("Synthèse de l'Outillage")
    if 'num_moyens' in st.session_state:
        total_outillage = sum(float(st.session_state.get(f"prix_tot_{i + 1}", 0)) for i in range(st.session_state.num_moyens))
        outillage_data = []
        for i in range(st.session_state.num_moyens):
            designation = st.session_state.get(f"designation_{i+1}", "None")
            fournisseur = st.session_state.get(f"fournisseur_{i+1}", "None")
            ref_fournisseur = st.session_state.get(f"ref_fournisseur_{i+1}", "None")
            quantite = st.session_state.get(f"quantite_{i+1}", 0)
            prix_uni = st.session_state.get(f"prix_uni_{i+1}", 0.0)
            prix_tot = st.session_state.get(f"prix_tot_{i+1}", 0.0)
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

    # Convert to DataFrame
    offre_df = pd.DataFrame(offre_data, columns=["Élément", "Valeur"])
    
    # Ensure all columns are strings
    for col in offre_df.columns:
        offre_df[col] = offre_df[col].astype(str)

    st.table(offre_df)

