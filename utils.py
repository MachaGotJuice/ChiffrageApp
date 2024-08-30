import os
import ast
import streamlit as st

def read_parameters_file(file_name):
    # Determine the directory of the current script
    script_dir = os.path.dirname(__file__)
    
    # Create the full file path
    file_path = os.path.join(script_dir, file_name)

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
        st.error(f"Le fichier {file_name} est introuvable.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
    return params, operations

def calculate_dmh(temps_seconds):
    """
    Converts time in seconds to DMH (dimillième d'heure).
    1 DMH = 1000th of an hour
    """
    return temps_seconds / 3600 * 1000


def calculate_total_time(sum_of_temps_coeff, correction_difficulte, setup_time, setup_quantity):
    """
    Calculates the total time using the formula:
    total_time = (sum of coefficient * temps) * (1 + correction difficulté) * (1 + setup_time / setup_quantity)
    """
    return sum_of_temps_coeff * (1 + correction_difficulte / 100) * (1 + setup_time / setup_quantity)


def calculate_time_per_wire(total_time, setup_quantity):
    """
    Calculates the time per wire.
    """
    return total_time / setup_quantity


def calculate_prix_unitaire(total_time, taux_horaire):
    """
    Calculates the unit price based on total time and hourly rate.
    prix_unitaire = total_time * taux_horaire / 3600
    """
    return total_time * taux_horaire / 3600
