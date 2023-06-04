import pickle
from django.conf import settings
import os

def getSentiment(sentence):
    # Load the sentiment analysis model from a pickle file
    model_path = os.path.join(settings.BASE_DIR, 'helpers/SentimentAnalysis.pickle')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Predict the sentiment of the sentence using the loaded model
    negative,positive,neutral,compound,overall_sentiment = model.predict([sentence])

    return negative,positive,neutral,compound,overall_sentiment 