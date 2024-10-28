import openai
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

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
    bmr = 88.362 + (13.397 * donnees.poids) + (4.799 * donnees.taille) - (5.677 * donnees.age)
    
    prompt = f"Créer un programme alimentaire pour une personne de {donnees.age} ans."

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=300
)


    programme_alimentaire = response.choices[0].text.strip()
    return {
        "calories_journalières": bmr,
        "programme_alimentaire": programme_alimentaire
    }


