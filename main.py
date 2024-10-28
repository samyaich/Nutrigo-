# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Configurez la clé d'API OpenAI depuis la variable d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

# Modèle de données pour recevoir les données du formulaire
class FormData(BaseModel):
    age: int
    poids: float
    taille: float
    sexe: str
    objectif: str
    preferences: list

# Endpoint de test basique pour vérifier si l'API est en ligne
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Endpoint de vérification de statut
@app.get("/status")
async def status():
    return {"status": "API is running"}

# Fonction de calcul du BMR (taux métabolique de base)
def calculer_bmr(age, poids, taille, sexe):
    if sexe == "homme":
        return 88.362 + (13.397 * poids) + (4.799 * taille) - (5.677 * age)
    else:
        return 447.593 + (9.247 * poids) + (3.098 * taille) - (4.330 * age)

# Fonction pour ajuster les besoins caloriques en fonction de l'objectif
def ajuster_besoins_caloriques(bmr, objectif):
    if objectif == "perte de poids":
        return bmr * 0.8
    elif objectif == "gain de muscle":
        return bmr * 1.2
    return bmr

# Endpoint principal pour générer un programme alimentaire
@app.post("/genererProgramme")
async def generer_programme_alimentaire(donnees: FormData):
    # Calculer le BMR et ajuster les besoins caloriques
    bmr = calculer_bmr(donnees.age, donnees.poids, donnees.taille, donnees.sexe)
    besoins_caloriques = ajuster_besoins_caloriques(bmr, donnees.objectif)

    # Préparer le prompt pour OpenAI
    prompt = (
        f"Créé un programme alimentaire pour une personne de {donnees.age} ans, "
        f"poids {donnees.poids} kg, taille {donnees.taille} cm, objectif {donnees.objectif}, "
        f"préférences alimentaires: {', '.join(donnees.preferences)}. "
        f"Calories quotidiennes: {besoins_caloriques:.2f}."
    )

    # Appel à l'API OpenAI en utilisant ChatCompletion
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en nutrition."},
                {"role": "user", "content": prompt}
            ]
        )
        programme_alimentaire = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return {"error": str(e)}

    # Retourner le programme alimentaire généré par OpenAI
    return {
        "calories_journalières": besoins_caloriques,
        "programme_alimentaire": programme_alimentaire
    }


