#Recherche des sentiments via Azure Text Analytics Cognitive Service
#Cette classe est une ébauche où les routines seront intégrées dans d'autres classes
#Auteur : Nicolas Campion
#Dernière mise à jour : 17 septembre 2020


import requests
import os

#Extraction des données du json généré par Azure Text Analytics Cognitive Service
def traitement_Data_IA():
    for j in sentiments["documents"]:
        for repere, valeur in j.items(): 
            if (repere == 'id'):
                valeurId = valeur
            if (repere == 'sentences'):
                for k in valeur:
                    for repere2, valeur2 in k.items(): 
                        if (repere2 == 'confidenceScores'):
                            for l in valeur2:
                                valeurPositive = valeur2['positive']
                                valeurNeutral = valeur2['neutral']
                                valeurNegative = valeur2['negative']
                        if (repere2 == 'length'):
                            valeurLength = valeur2
                        if (repere2 == 'offset'):
                            valeurOffset = valeur2
                        if (repere2 == 'sentiment'):
                            valeurSentiment = valeur2
                        if (repere2 == 'text'):
                            valeurText = valeur2
            if (repere == 'sentiment'): 
                valeurSentimentFinal = valeur

        resultat.append({"id": valeurId, 
                        "text": valeurText,
                        "length": valeurLength,
                        "offset": valeurOffset, 
                        "sentiment": valeurSentiment,
                        "sentiments": valeurSentimentFinal,
                        "positive": valeurPositive,
                        "neutral": valeurNeutral,
                        "negative": valeurNegative})

liste = []
resultat = []

#Ces variables sont essentielles pour se connecter à Azure Text Ananlytics
subscription_key = "c42ac7b0e0944f748407efd276d748ff"
endpoint = "https://cs-groupe-trois.cognitiveservices.azure.com/"

#Ici, seul l'analyse de sentiments est nécessaire
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

#Cette variable doit être remplacée par le bon fichier json
documentJson = {"documents": [
    {"id": "1", "language": "fr",
        "text": "Je suis content."},
    {"id": "2", "language": "fr",
        "text": "Cela ne me fait ni chaud, ni froid."},
    {"id": "3", "language": "fr",
        "text": "Ca me donne envie d'hurler"},
    {"id": "4", "language": "fr",
        "text": "Comment ça va ?"}
]}

#Appel d'Azure
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_url, headers=headers, json=documentJson)
sentiments = response.json()

#Appel de la fonction
traitement_Data_IA()

print (resultat)