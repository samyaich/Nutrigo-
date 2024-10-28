# main.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modèle de données pour recevoir les données du formulaire
class FormData(BaseModel):
    age: int
    poids: float
    taille: float
    sexe: str
    objectif: str
    preferences: list

def calculer_bmr(age, poids, taille, sexe):
    # Calcul simple du métabolisme de base (BMR)
    if sexe == "homme":
        return 88.362 + (13.397 * poids) + (4.799 * taille) - (5.677 * age)
    else:
        return 447.593 + (9.247 * poids) + (3.098 * taille) - (4.330 * age)

def ajuster_besoins_caloriques(bmr, objectif):
    if objectif == "perte de poids":
        return bmr * 0.8
    elif objectif == "gain de muscle":
        return bmr * 1.2
    return bmr

@app.post("/genererProgramme")
async def generer_programme_alimentaire(donnees: FormData):
    # Calcule le BMR et ajuste les besoins caloriques
    bmr = calculer_bmr(donnees.age, donnees.poids, donnees.taille, donnees.sexe)
    besoins_caloriques = ajuster_besoins_caloriques(bmr, donnees.objectif)

    # Logique de génération de menu simplifiée
    programme = {
        "petit_dejeuner": "Omelette et fruits",
        "dejeuner": "Salade avec protéine maigre",
        "diner": "Poisson avec légumes",
        "collation": "Yaourt grec et noix",
        "calories_journalières": besoins_caloriques
    }

    return programme
