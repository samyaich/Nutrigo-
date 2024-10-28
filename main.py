import openai
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

# Configuration de la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class FormData(BaseModel):
    age: int
    poids: float
    taille: float
    sexe: str
    objectif: str
    preferences: list

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/genererProgramme")
async def generer_programme_alimentaire(donnees: FormData):
    # Exemple simplifié de calcul de BMR
    bmr = 88.362 + (13.397 * donnees.poids) + (4.799 * donnees.taille) - (5.677 * donnees.age)
    
    # Préparer le prompt pour OpenAI
    prompt = f"Créer un programme alimentaire pour une personne de {donnees.age} ans."

    # Appel correct à l'API OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un expert en nutrition."},
            {"role": "user", "content": prompt}
        ]
    )

    programme_alimentaire = response.choices[0].message['content']
    return {
        "calories_journalières": bmr,
        "programme_alimentaire": programme_alimentaire
    }


