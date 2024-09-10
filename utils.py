# utils.py

def read_parameters():
    """
    Imports and returns the operations_times dictionary from the parametres.py module.
    """
    from parametres import operations_times
    return operations_times

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
