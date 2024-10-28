from flask import Flask, request, jsonify
from textblob import TextBlob

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir une route pour l'analyse des sentiments
@app.route('/analyse-sentiment', methods=['POST'])
def analyse_sentiment():
    # Récupérer les données JSON envoyées dans la requête
    data = request.get_json()

    # Vérifier si le commentaire est présent dans les données et n'est pas vide
    commentaire = data.get('commentaire', '')
    if not commentaire:
        return jsonify({'erreur': 'Le commentaire est manquant ou vide'}), 400

    # Analyser le sentiment du commentaire avec TextBlob
    analyse = TextBlob(commentaire)
    ton = analyse.sentiment.polarity

    # Déterminer le ton du commentaire
    if ton > 0:
        sentiment = 'Positive'
    elif ton < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    # Renvoyer le résultat de l'analyse des sentiments au format JSON
    return jsonify({'sentiment': sentiment}), 200

# Point d'entrée de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
