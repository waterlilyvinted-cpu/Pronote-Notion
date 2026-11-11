import os
import datetime
import pronotepy
from notion_client import Client

# Récupération des secrets
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
PRONOTE_URL = os.environ.get("PRONOTE_URL", "").strip()
PRONOTE_USERNAME = os.environ.get("PRONOTE_USERNAME", "").strip()
PRONOTE_PASSWORD = os.environ.get("PRONOTE_PASSWORD", "").strip()

def sync():
    notion = Client(auth=NOTION_TOKEN)
    
    # Nettoyage automatique de l'URL si besoin
    url = PRONOTE_URL
    if not url.endswith("/"):
        url += "/"
    if url.endswith("eleve.html/"):
        url = url.replace("eleve.html/", "")

    print(f"Connexion à Pronote sur : {url}")
    
    try:
        # Connexion directe à l'élève
        client = pronotepy.Client(url + "eleve.html", username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD)
    except Exception as e:
        print(f"Échec de connexion directe, tentative avec l'URL de base : {e}")
        client = pronotepy.Client(url, username=PRONOTE_USERNAME, password=PRONOTE_PASSWORD)

    if not client.logged_in:
        print("Erreur : Impossible de se connecter à Pronote. Vérifiez vos identifiants.")
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
