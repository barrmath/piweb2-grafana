# telecharge traite les données puis sauvegarde pour grafana

import wget
import pandas as pd
import numpy as np

# téléchargement des données

print("téléchargement des données")
URL_IPS = "https://www.data.gouv.fr/fr/datasets/r/28e511a7-af0d-48c7-a8bb-2f38ec003f49"
URL_effectifs = (
    "https://www.data.gouv.fr/fr/datasets/r/6bf59bae-3c3b-40f5-ad8e-f05b0b2ac271"
)
URL_VA = "https://www.data.gouv.fr/fr/datasets/r/a230247a-8aea-4112-be41-bc008c0d6966"
print("telechargement fichier IPS")
response = wget.download(URL_IPS, "donnee/IPS.csv")
print("\ntelechargement fichier effectifs")
response = wget.download(URL_effectifs, "donnee/effectifs.csv")
print("\ntelechargement fichier VA")
response = wget.download(URL_VA, "donnee/VA.csv")

# traitement des données pour en savoir plus : https://github.com/barrmath/data_educ

print("\ntraitement en cours")
IPS = pd.read_csv("donnee/IPS.csv", sep=";")
effectifs = pd.read_csv("donnee/effectifs.csv", sep=";", low_memory=False)
VA = pd.read_csv("donnee/VA.csv", sep=";")

VA["Taux d'accès 6ème-3ème"] = VA["Taux d'accès 6ème-3ème"].replace("ND", np.nan)
VA["Taux d'accès 6ème-3ème"] = VA["Taux d'accès 6ème-3ème"].astype("float")
VA.rename(columns={"Session": "Rentrée scolaire"}, inplace=True)
VA["Rentrée scolaire"] = VA["Rentrée scolaire"] - 1
VA.drop(
    columns=[
        "Nom de l'établissement",
        "Commune",
        "Département",
        "Académie",
        "Secteur",
    ],
    inplace=True,
)
IPS["Secteur"] = IPS["Secteur"].replace(
    {"public": "PUBLIC", "privé sous contrat": "PRIVE"}
)
IPS["Rentrée scolaire"] = IPS["Rentrée scolaire"].str[:4].astype("int")
effectifs.rename(columns={"Numéro du collège": "UAI"}, inplace=True)
fichier_college = pd.merge(effectifs, IPS, on=["Rentrée scolaire", "UAI"], how="outer")
fichier_college.drop(columns=["Académie_y", "Département_y", "Secteur_y"], inplace=True)
fichier_college.rename(
    columns={
        "Académie_x": "Académie",
        "Département_x": "Département",
        "Secteur_x": "Secteur",
    },
    inplace=True,
)
fichier_college["6èmes LV2 autres langues"] = ""
langue = [
    "èmes LV1 allemand",
    "èmes LV1 anglais",
    "èmes LV1 espagnol",
    "èmes LV1 autres langues",
    "èmes LV2 allemand",
    "èmes LV2 anglais",
    "èmes LV2 espagnol",
    "èmes LV2 italien",
    "èmes LV2 autres langues",
]
for a in range(3, 7, 1):
    for b in langue:
        fichier_college.drop(columns=str(a) + b, inplace=True)

fichier_college = pd.merge(
    fichier_college, VA, on=["Rentrée scolaire", "UAI"], how="outer"
)

fichier_college.drop(
    columns=["Nom de la commune", "Nom de l'établissment", "Code du département"],
    inplace=True,
)
fichier_college["Pourcentage Ulis sur le nombre d'eleves total"] = (
    fichier_college["Nombre d'élèves total ULIS"]
    / fichier_college["Nombre d'élèves total"]
    * 100
)


# sauvegarde pour grafana

fichier_college.to_csv("donnee/college.csv", index=False)
