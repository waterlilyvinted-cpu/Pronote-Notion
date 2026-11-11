import os
import datetime
import pronotepy
from notion_client import Client

# Récupération des secrets GitHub
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
PRONOTE_URL = os.environ.get("PRONOTE_URL", "").strip()
PRONOTE_USERNAME = os.environ.get("PRONOTE_USERNAME", "").strip()
PRONOTE_PASSWORD = os.environ.get("PRONOTE_PASSWORD", "").strip()

def sync():
    notion = Client(auth=NOTION_TOKEN)
    
    # S'assurer que l'URL se termine bien par un slash /
    url = PRONOTE_URL
    if not url.endswith("/"):
        url += "/"

    print(f"Connexion à Pronote sur : {url}")
    
    # Connexion directe Pronote (sans ENT)
    client = pronotepy.Client(url + "eleve.html", username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD)

    if not client.logged_in:
        print("Erreur : Connexion impossible. Vérifiez identifiant et mot de passe.")
        return

    print("Connexion réussie ! Récupération des devoirs...")
    today = datetime.date.today()
    homeworks = client.homework(today)

    for hw in homeworks:
        subject = hw.subject.name
        description = hw.description
        due_date = hw.date.strftime("%Y-%m-%d")

        print(f"Ajout : {subject} pour le {due_date}")

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
