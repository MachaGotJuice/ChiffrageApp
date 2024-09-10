import streamlit as st
from utils import read_parameters, calculate_dmh, calculate_total_time, calculate_time_per_wire, calculate_prix_unitaire

def initialize_session_state_key(key, default_value):
    """Initialize a session state key with a default value if it doesn't exist."""
    if key not in st.session_state:
        st.session_state[key] = default_value

def gamme_page():
    st.title("Gamme")

    # Load operations from parametres.py using the utility function
    operations_times = read_parameters()

    # Ensure num_items is initialized in session state
    if 'num_items' not in st.session_state:
        st.session_state.num_items = 1

    # Ensure operations and coefficients are initialized in session state
    if 'operations' not in st.session_state:
        st.session_state.operations = {i: [] for i in range(st.session_state.num_items)}

    if 'coefficients' not in st.session_state:
        st.session_state.coefficients = {i: {} for i in range(st.session_state.num_items)}

    # Iterate over items and ensure each key is initialized
    for i in range(st.session_state.num_items):
        item_name_key = f"item_name_{i+1}"
        ref_plan_key = f"reference_plan_{i+1}"
        descriptif_key = f"descriptif_{i+1}"
        nombre_fils_key = f"nombre_fils_{i+1}"
        quantite_key = f"quantite_{i+1}"
        quantite_optionnelle_key = f"quantite_optionnelle_{i+1}"
        correction_difficulte_key = f"correction_difficulte_{i+1}"
        setup_time_key = f"setup_time_{i+1}"
        setup_quantity_key = f"setup_quantity_{i+1}"

        # Initialize keys with default values if they don't exist
        initialize_session_state_key(item_name_key, "")
        initialize_session_state_key(ref_plan_key, "")
        initialize_session_state_key(descriptif_key, "")
        initialize_session_state_key(nombre_fils_key, 0)
        initialize_session_state_key(quantite_key, 0)
        initialize_session_state_key(quantite_optionnelle_key, 0)
        initialize_session_state_key(correction_difficulte_key, 20.0)
        initialize_session_state_key(setup_time_key, 2.0)
        initialize_session_state_key(setup_quantity_key, 10000)

        with st.expander(f"Item {i+1}"):
            # Collecting item-specific details and updating session state
            st.session_state[item_name_key] = st.text_input("Nom de l'item", value=st.session_state[item_name_key], key=f"item_name_blank{i+1}")
            st.session_state[ref_plan_key] = st.text_input("Reference Plan", value=st.session_state[ref_plan_key], key=f"ref_plan_blank{i+1}")
            st.session_state[descriptif_key] = st.text_input("Descriptif", value=st.session_state[descriptif_key], key=f"descriptif_blank{i+1}")
            st.session_state[nombre_fils_key] = st.number_input("Nombre de fils", min_value=0, value=st.session_state[nombre_fils_key], key=f"nombre_fils_blank{i+1}")
            st.session_state[quantite_key] = st.number_input("Quantité", min_value=0, value=st.session_state[quantite_key], key=f"quantite_blank{i+1}")
            st.session_state[quantite_optionnelle_key] = st.number_input("Quantité optionnelle", min_value=0, value=st.session_state[quantite_optionnelle_key], key=f"quantite_optionnelle_blank{i+1}")

            # Inputs for correction difficulté, setup time, and setup quantity
            st.session_state[correction_difficulte_key] = st.number_input(
                "Correction difficulté (%)", min_value=0.0, max_value=100.0, value=st.session_state[correction_difficulte_key], step=1.0, key=f"correction_difficulte_blank{i+1}"
            )
            st.session_state[setup_time_key] = st.number_input(
                "Setup Time (heures)", min_value=0.0, value=st.session_state[setup_time_key], step=0.5, key=f"setup_time_blank{i+1}"
            )
            st.session_state[setup_quantity_key] = st.number_input(
                "Setup Quantity", min_value=1, value=st.session_state[setup_quantity_key], step=100, key=f"setup_quantity_blank{i+1}"
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

            to_delete = None
            for j, op in enumerate(st.session_state.operations[i]):
                temps = operations_times.get(op, 0)
                coeff = st.session_state.coefficients[i].get(op, 1.0)
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
                    st.session_state.coefficients[i][op] = coeff  # Update coefficient in session state
                with col5:
                    if st.button("X", key=f"delete_op_button_{i+1}_{j}"):
                        to_delete = j

                # Accumulate the sum of coefficient * temps
                sum_of_temps_coeff += temps * coeff

            if to_delete is not None:
                del st.session_state.operations[i][to_delete]

            selected_operation = st.selectbox(
                "Sélectionner une opération",
                list(operations_times.keys()),
                key=f"operation_select_{i+1}"
            )
            if st.button("Ajouter opération", key=f"add_op_button_{i+1}"):
                if selected_operation not in st.session_state.operations[i]:
                    st.session_state.operations[i].append(selected_operation)
                    st.session_state.coefficients[i][selected_operation] = 1.0
                    st.success(f"Opération '{selected_operation}' ajoutée.")

            # Calculate total time using the utility function
            total_time = calculate_total_time(sum_of_temps_coeff, st.session_state[correction_difficulte_key], st.session_state[setup_time_key], st.session_state[setup_quantity_key])

            # Calculate time per wire and unit price using utility functions
            time_per_wire = calculate_time_per_wire(total_time, st.session_state[setup_quantity_key])
            taux_horaire = 50  # Example hourly rate in euros
            prix_unitaire = calculate_prix_unitaire(total_time, taux_horaire)

            # Display computed results for this item
            st.subheader("Résultats")
            st.write(f"Temps total (s): {total_time:.2f}")
            st.write(f"Temps par fil (s): {time_per_wire:.4f}")
            st.write(f"Prix Unitaire (€): {prix_unitaire:.2f}")

    # Button to add a new item
    if st.button("+ Ajouter un item"):
        st.session_state.num_items += 1
        st.session_state.operations[st.session_state.num_items - 1] = []
        st.session_state.coefficients[st.session_state.num_items - 1] = {}
