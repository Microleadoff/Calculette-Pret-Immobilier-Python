"""Import des modules"""
import re  # expressions régulières
import os  # gérer le système de fichiers
from fpdf import FPDF  # export PDF avec PyFPDF
# Installation de la biblothèque : pip install fpdf
# extension pour visualisation ds VsCode : vscode-pdf

def print_error(text):
    """Affiche du texte en rouge dans le terminal."""
    print("\033[91m" + text + "\033[0m")

def get_valid_amount_input():
    """
    Demande à l'utilisateur un montant de prêt valide en euros.

    Returns:
        int: Montant du prêt en euros.
    """
    while True:
        amount = input("Montant du prêt en euros : ")
        if re.match(r'^(?!0+$)\d+$', amount):
            return int(amount)
        else:
            print_error("Montant invalide. Veuillez réessayer.")

def get_valid_rate_input():
    """
    Demande à l'utilisateur un taux d'intérêt nominal annuel valide.

    Returns:
        float: Taux d'intérêt nominal annuel.
    """
    while True:
        rate = input("Taux d'intérêt nominal annuel : ")
        if re.match(r'^(?!0$)([1-9]\d{0,1}([.,]\d{1,2})?|0[.,]\d{1,2})$', rate):
            return float(rate)
        else:
            print_error("Taux d'intérêt invalide. Veuillez réessayer.")

def get_valid_duration_input():
    """
    Demande à l'utilisateur une durée de prêt en années valide.

    Returns:
        int: Durée du prêt en années.
    """
    while True:
        duration = input("Durée du prêt en années : ")
        if re.match(r'^[1-9](\d){0,1}$', duration):
            return int(duration)
        else:
            print_error("Durée invalide. Veuillez réessayer.")

def data_recovery():
    """
    Demande les données du prêt à l'utilisateur (montant, taux, durée) et les valide.

    Returns:
        Tuple[int, float, int]: Un tuple contenant le montant, le taux d'intérêt, et la durée.
    """
    while True:
        amount = get_valid_amount_input()
        rate = get_valid_rate_input()
        duration = get_valid_duration_input()
        return amount, rate, duration

def display_titles():
    """Affiche les titres des colonnes pour les résultats."""
    print("\nTableau d'Amortissement :\n")
    print(
        "Mois | Montant initial |   EMI   | "\
        "Intérêts  | Amortissement  | Montant final "
    )
    print("-" * 80)  # Ligne de séparation

def display_result(values):
    """
    Affiche les résultats de l'amortissement.

    Args:
        values (List): Une liste contenant les valeurs à afficher.
    """
    # mise en forme en fonction du nb de caractères
    print(
        f"{values[0]:<4} | {values[1]:>13} € |{values[2]:>6} € | "\
        f"{values[3]:>7} € |{values[4]:>12} € | {values[5]:>12} €"
    )

def generate_unique_filename(base_filename, extension):
    """
    Génère un nom de fichier unique en ajoutant un numéro incrémental
    entre parenthèses s'il existe déjà.

    Args:
        base_filename (str): Le nom de base du fichier.
        extension (str): L'extension du fichier (par exemple, ".pdf").

    Returns:
        str: Le nom de fichier unique.
    """
    download_dir = "download"  # nom du répertoire de téléchargement
    os.makedirs(download_dir, exist_ok=True) # crée le répertoire s'il n'existe pas

    filename = f"{base_filename}{extension}"  # nom du fichier de base
    file_path = os.path.join(download_dir, filename)  # construit le chemin complet du fichier
    # vérifie si le fichier existe et incrémente le numéro si nécessaire
    file_exists = True
    file_number = 0
    while file_exists:
        if os.path.exists(file_path):  # vérifie si un fichier existe à l'emplacement spécifié
            file_number += 1
            filename = f"{base_filename}({file_number}){extension}"
            # créer un chemin complet vers le fichier
            file_path = os.path.join(download_dir, filename)
        else:
            file_exists = False

    return file_path  # retourne le chemin complet du fichier

def export_to_pdf(data, values):
    """
    Exporte les résultats dans un fichier PDF.

    Args:
        data (List[List]): Une liste contenant les données en entrée.
        values (List[List]): Une liste contenant les données de l'amortissement.
    """
    base_filename = "calcul_amortissement"  # nom de base du fichier PDF
    extension = ".pdf"
    filename = generate_unique_filename(base_filename, extension)  # génère un nom de fichier unique

    pdf = FPDF()  # crée un objet PDF
    pdf.add_page()  # ajoute une page à votre document
    pdf.set_fill_color(35, 75, 104)  # défini la couleur de remplissage

    pdf.image("logo_microlead.png", x=(210-30)/2, y=10, w=30, h=10)  # ajoutez le logo
    pdf.ln(20)  # saut de ligne

    # affiche les données entrées par l'utilisateur
    pdf.set_font('Arial', 'B', 14)  # définit la police et la taille
    pdf.cell(0, 10, "Données d'Amortissement", 0, 0, "C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Montant du prêt : {data[0]} Euros")
    pdf.multi_cell(0, 10, f"Taux d'intérêt annuel : {data[1]} %")
    pdf.multi_cell(0, 10, f"Durée du prêt : {data[2]} années")
    pdf.ln(10)

    # titre de la deuxième partie
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "Tableau d'Amortissement", 0, 0, "C")
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, "Les montants sont exprimés en Euros", 0, 0, "C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    # en-tête du tableau
    pdf.cell(15, 10, "Mois", "B", 0, "R")
    pdf.cell(35, 10, "Montant initial", "B", 0, "R")
    pdf.cell(35, 10, "EMI", "B", 0, "R")
    pdf.cell(35, 10, "Intérêts", "B", 0, "R")
    pdf.cell(35, 10, "Amortissement", "B", 0, "R")
    pdf.cell(35, 10, "Montant final", "B", 0, "R")
    pdf.ln()

    # donnée calculées de l'amortissement
    for row in values:
        pdf.cell(15, 10, str(row[0]), 0, 0, "R")  # Mois
        pdf.cell(35, 10, str(row[1]), 0, 0, "R")  # Montant initial
        pdf.cell(35, 10, str(row[2]), 0, 0, "R")  # EMI
        pdf.cell(35, 10, str(row[3]), 0, 0, "R")  # Intérêts
        pdf.cell(35, 10, str(row[4]), 0, 0, "R")  # Amortissement
        pdf.cell(35, 10, str(row[5]), 0, 0, "R")  # Montant final
        pdf.ln()

    pdf.output(filename)  # enregistre le file
    print(f"\033[92mLes résultats ont été exportés dans {filename}\033[0m")

def amortization_calculation(amount, rate, duration):
    """
    Calcule l'amortissement et affiche les résultats.

    Args:
        amount (int): Montant du prêt en euros.
        rate (float): Taux d'intérêt nominal annuel.
        duration (int): Durée du prêt en années.
    
    Returns:
        List[List]: Une liste contenant les données d'amortissement.
    """
    amortization_data = []  # Créez une liste pour stocker les données d'amortissement
    decimal_month_rate = (rate / 12) / 100  # calcul du taux d'intérêt mensuel en décimal
    number_of_payments = duration * 12  # calcul du nombre de mensualités
    # calcul de l'échéance mensuelle
    emi = round(
        amount * (decimal_month_rate * ((1 + decimal_month_rate) ** number_of_payments) /
        (((1 + decimal_month_rate) ** number_of_payments) - 1))
    )

    # Vérification si l'échéance est inférieure à 10 euro
    if emi < 10:
        print_error(
            "L'échéance mensuelle est inférieure à 10 euro. "\
            "Veuillez saisir de nouvelles données !"
        )
        launch_script()  # relance le script

    # déclaration et initialisation des variables
    month = 1
    initial_amount = int(round(amount))
    interest = 0
    amortization = 0
    final_amount = 0
    # affiche les titres une fois au début
    display_titles()

    # boucle tant que la somme à rembourser est supérieur à 0
    while True :
        interest = round(initial_amount * decimal_month_rate)  # calcul des intérêts
        amortization = round(emi - interest)  # calcul de l'amortissement
        # dernière ligne d'amortissement
        if emi >= initial_amount or month == number_of_payments:
            final_amount = 0
            emi = initial_amount + interest  # recalcul de l'échéance
            amortization = round(emi - interest)  # recalcul de l'amortissement
        else:
            final_amount = round(initial_amount - amortization)

        # stock les données d'amortissement
        amortization_data.append(
            [month, initial_amount, emi,
            interest, amortization, final_amount]
        )
        # appel de la fonction pour display le résultat
        display_result(amortization_data[-1])

        month += 1
        initial_amount = final_amount
        # permet de simuler une boucle Do While
        if final_amount <= 0:
            break

    # Retournez la liste contenant les données d'amortissement
    return amortization_data

def export_simulation():
    """
    Demande à l'utilisateur s'il souhaite exporter les résultats en PDF.

    Returns:
        bool: True si l'utilisateur choisit 'O' (oui), False s'il choisit 'N' (non).
    """
    while True:
        choice = input(
            "\033[93mVoulez-vous exporter les résultats en PDF ? "\
            "(O/N)\033[0m"
        ).strip().upper()

        if choice == "O":
            return True
        elif choice == "N":
            return False
        else:
            print_error("Choix invalide. Veuillez répondre par 'O' pour oui ou 'N' pour non.")

def replay_simulation():
    """
    Demande à l'utilisateur s'il souhaite effectuer une autre simulation.

    Returns:
        bool: True si l'utilisateur choisit 'O' (oui), False s'il choisit 'N' (non).
    """
    while True:
        choice = input(
            "\033[93mVoulez-vous effectuer une autre simulation ? "\
            "(O/N)\033[0m"
        ).strip().upper()

        if choice == "O":
            return True
        elif choice == "N":
            return False
        else:
            print_error("Choix invalide. Veuillez répondre par 'O' pour oui ou 'N' pour non.")

def launch_script():
    """Fonction principale pour lancer le script de calcul d'amortissement de prêt."""
    print("Bienvenu chez Microlead pour votre simulation de calcul d'amortissement de prêt")
    while True:
        # appeler la fonction de récupération de données
        data = data_recovery()
        if data:
            # appeler la fonction de calcul si les données sont bonnes
            data_calculated = amortization_calculation(data[0], data[1], data[2])

            # Demander à l'utilisateur s'il souhaite exporter en PDF
            if export_simulation():
                export_to_pdf(data, data_calculated)

        # Demande à l'utilisateur s'il souhaite effectuer une autre simulation
        if not replay_simulation():
            # Si l'utilisateur choisit de ne pas continuer, sort de la boucle
            break

launch_script()
