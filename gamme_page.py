import streamlit as st
from utils import read_parameters_file, calculate_dmh, calculate_total_time, calculate_time_per_wire, calculate_prix_unitaire

def gamme_page():
    st.title("Gamme")

    # Load parameters
    params_file_name = "parametres.txt"
    params, operations = read_parameters_file(params_file_name)

    num_items = 1

    operations_data = {}
    coefficients_data = {}

    for i in range(num_items):
        with st.expander(f"Item {i+1}"):
            # Collecting item-specific details
            item_name = st.text_input("Nom de l'item", key=f"item_name_{i+1}")
            description = st.text_area("Description", key=f"description_{i+1}")
            ref_plan = st.text_input("Reference Plan", key=f"reference_plan_{i+1}")
            descriptif = st.text_input("Descriptif", key=f"descriptif_{i+1}")
            nombre_fils = st.number_input("Nombre de fils", min_value=0, key=f"nombre_fils_{i+1}")
            quantite = st.number_input("Quantité", min_value=0, key=f"quantite_{i+1}")
            quantite_optionnelle = st.number_input("Quantité optionnelle", min_value=0, key=f"quantite_optionnelle_{i+1}")

            # Inputs for correction difficulté, setup time, and setup quantity
            correction_difficulte = st.number_input(
                "Correction difficulté (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0, key=f"correction_difficulte_{i+1}"
            )
            setup_time = st.number_input(
                "Setup Time (heures)", min_value=0.0, value=2.0, step=0.5, key=f"setup_time_{i+1}"
            )
            setup_quantity = st.number_input(
                "Setup Quantity", min_value=1, value=10000, step=100, key=f"setup_quantity_{i+1}"
            )

            # Operation list with coefficient and time calculations
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                st.markdown("**Opération**")
            with col2:
                st.markdown("**Temps (s)**")
            with col3:
                st.markdown("**Temps (DMH)**")
            with col4:
                st.markdown("**Coefficient**")
            with col5:
                st.markdown("**Action**")

            sum_of_temps_coeff = 0  # Initialize sum for total time calculation

            if i not in operations_data:
                operations_data[i] = []
                coefficients_data[i] = {}

            to_delete = None
            for j, op in enumerate(operations_data[i]):
                temps = operations.get(op, 0)
                coeff = coefficients_data[i].get(op, 1.0)
                dmh = calculate_dmh(temps)  # Using utility function to calculate DMH
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"{j + 1}. {op}")
                with col2:
                    st.write(f"{temps}")
                with col3:
                    st.write(f"{dmh:.2f}")
                with col4:
                    coeff = st.number_input(
                        "Coefficient",
                        min_value=0.0,
                        value=coeff,
                        step=0.1,
                        key=f"coeff_{i}_{j}",
                        label_visibility="collapsed",
                        format="%.2f"
                    )
                    coefficients_data[i][op] = coeff
                with col5:
                    if st.button("X", key=f"delete_op_button_{i+1}_{j}"):
                        to_delete = j

                # Accumulate the sum of coefficient * temps
                sum_of_temps_coeff += temps * coeff

            if to_delete is not None:
                del operations_data[i][to_delete]

            selected_operation = st.selectbox(
                "Sélectionner une opération",
                list(operations.keys()),
                key=f"operation_select_{i+1}"
            )
            if st.button("Ajouter opération", key=f"add_op_button_{i+1}"):
                if selected_operation not in operations_data[i]:
                    operations_data[i].append(selected_operation)
                    coefficients_data[i][selected_operation] = 1.0
                    st.success(f"Opération '{selected_operation}' ajoutée.")

            # Calculate total time using the utility function
            total_time = calculate_total_time(sum_of_temps_coeff, correction_difficulte, setup_time, setup_quantity)

            # Calculate time per wire and unit price using utility functions
            time_per_wire = calculate_time_per_wire(total_time, setup_quantity)
            taux_horaire = 50  # Example hourly rate in euros
            prix_unitaire = calculate_prix_unitaire(total_time, taux_horaire)

            # Display computed results for this item
            st.subheader("Résultats")
            st.write(f"Temps total (s): {total_time:.2f}")
            st.write(f"Temps par fil (s): {time_per_wire:.4f}")
            st.write(f"Prix Unitaire (€): {prix_unitaire:.2f}")

    # Button to add a new item
    if st.button("+ Ajouter un item"):
        num_items += 1
        operations_data[num_items - 1] = []
        coefficients_data[num_items - 1] = {}

