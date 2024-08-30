import ast
import streamlit as st
def read_parameters_file(file_path):
    params = {}
    operations = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    if key.strip() == 'operations':
                        operations = ast.literal_eval(value.strip())
                    else:
                        params[key.strip()] = value.strip()
    except FileNotFoundError:
        st.error(f"Le fichier {file_path} est introuvable.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
    return params, operations

def write_parameters_file(file_path, params):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for key, value in params.items():
                if isinstance(value, dict):
                    file.write(f"{key}={value}\n")
                else:
                    file.write(f"{key}={value}\n")
    except Exception as e:
        st.error(f"Erreur lors de l'écriture du fichier : {e}")
