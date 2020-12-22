import os

ENDPOINT = "https://sasquatch.cognitiveservices.azure.com/"
ENDPOINT_PRED = "https://sasquatch-prediction.cognitiveservices.azure.com/"

TRAINING_KEY = os.environ.get("TRAINING_KEY")
PREDICTION_KEY = os.environ.get("PREDICTION_KEY")
PREDICTION_RESOURCE_ID = os.environ.get("PREDICTION_RESOURCE_ID")

CV_BATCH_SIZE = 64
