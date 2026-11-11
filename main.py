import os
import datetime
import pronotepy
from pronotepy.ent import *
from notion_client import Client

# 1. Récupération des secrets GitHub
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
PRONOTE_URL = os.environ.get("PRONOTE_URL")
PRONOTE_USERNAME = os.environ.get("PRONOTE_USERNAME")
PRONOTE_PASSWORD = os.environ.get("PRONOTE_PASSWORD")

def sync():
    # Initialisation du client Notion
    notion = Client(auth=NOTION_TOKEN)
    
    print("Connexion à Pronote...")
    # Connexion à Pronote (connexion directe sans ENT)
    client = pronotepy.Client(PRONOTE_URL, username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD)
    
    if not client.logged_in:
        print("Échec de la connexion à Pronote.")
        return

    print("Connexion réussie ! Récupération des devoirs...")
    # Récupération des devoirs à partir d'aujourd'hui
    today = datetime.date.today()
    homeworks = client.homework(today)

    for hw in homeworks:
        subject = hw.subject.name
        description = hw.description
        due_date = hw.date.strftime("%Y-%m-%d")

        print(f"Ajout du devoir : {subject} pour le {due_date}")

        # Envoi de chaque devoir dans la base de données Notion
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Nom": {"title": [{"text": {"content": f"{subject} - Devoir"}}]},
                "Échéance": {"date": {"start": due_date}},
                "Description": {"rich_text": [{"text": {"content": description}}]}
            }
        )

if __name__ == "__main__":
    sync()
