from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

ENDPOINT = "https://sasquatch.cognitiveservices.azure.com/"
training_key = "93db553104c545d58f905ba4576e769b"
prediction_key = "c93878bffea849a2aed69f9c9aaffeba"
prediction_resource_id = '/subscriptions/c7c48690-c7a7-435b-b470-68599c1a2448/resourcegroups/azure-projekt/providers/Microsoft.CognitiveServices/accounts/sasquatch-Prediction'
ENDPOINT_PRED = "https://sasquatch-prediction.cognitiveservices.azure.com/"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

publish_iteration_name = "detectModel"

# Find the object detection domain
obj_detection_domain = next(domain for domain in trainer.get_domains() if domain.type == "ObjectDetection" and domain.name == "General")

# Create a new project
print ("Creating project...")
project = trainer.create_project("My Detection Project", domain_id=obj_detection_domain.id)

DATASET_PATH = '/home/jakub/Studia/Semestr7/azure/projekt/azure-project/data/'
base_image_location = DATASET_PATH

with open(base_image_location + "Images/test/test_image.jpg", mode="rb") as test_data:
    results = predictor.detect_image(project.id, publish_iteration_name, test_data)
