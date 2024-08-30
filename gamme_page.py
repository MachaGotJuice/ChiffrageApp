import streamlit as st

def gamme_page():
    st.title("Gamme")

    if 'num_items' not in st.session_state:
        st.session_state.num_items = 1

    if 'operations' not in st.session_state:
        st.session_state.operations = {i: [] for i in range(st.session_state.num_items)}

    if 'coefficients' not in st.session_state:
        st.session_state.coefficients = {i: {} for i in range(st.session_state.num_items)}

    for i in range(st.session_state.num_items):
        item_name_key = f"item_name_{i+1}"

        with st.expander(st.session_state.get(item_name_key, f"Item {i+1}")):
            item_name = st.text_input("Nom de l'item", key=item_name_key)
            description = st.text_area("Description", key=f"description_{i+1}")
            ref_plan = st.text_input("Reference Plan", key=f"reference_plan_{i+1}")
            descriptif = st.text_input("Descriptif", key=f"descriptif_{i+1}")
            nombre_fils = st.text_input("Nombre de fils", key=f"nombre_fils_{i+1}")
            quantite = st.text_input("Quantité", key=f"quantite_{i+1}")
            quantite_optionnelle = st.text_input("Quantité optionnelle", key=f"quantite_optionnelle_{i+1}")

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

            to_delete = None
            for j, op in enumerate(st.session_state.operations[i]):
                dmh = st.session_state.operations_times.get(op, 0) / 3600 * 1000
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"{j + 1}. {op}")
                with col2:
                    st.write(f"{st.session_state.operations_times.get(op, 0)}")
                with col3:
                    st.write(f"{dmh:.2f}")
                with col4:
                    st.number_input(
                        "Coefficient",
                        min_value=0.0,
                        value=st.session_state.coefficients[i].get(op, 1.0),
                        step=0.1,
                        key=f"coeff_{i}_{j}",
                        label_visibility="collapsed",
                        format="%.2f"
                    )
                with col5:
                    if st.button("X", key=f"delete_op_button_{i+1}_{j}"):
                        to_delete = j
            
            if to_delete is not None:
                del st.session_state.operations[i][to_delete]

            selected_operation = st.selectbox(
                "Sélectionner une opération",
                st.session_state.operations_list,
                key=f"operation_select_{i+1}"
            )
            if st.button("Ajouter opération", key=f"add_op_button_{i+1}"):
                if selected_operation not in st.session_state.operations[i]:
                    st.session_state.operations[i].append(selected_operation)
                    st.session_state.coefficients[i][selected_operation] = 1.0
                    st.success(f"Opération '{selected_operation}' ajoutée.")

    if st.button("+ Ajouter un item"):
        st.session_state.num_items += 1
        st.session_state.operations[st.session_state.num_items - 1] = []
        st.session_state.coefficients[st.session_state.num_items - 1] = {}

