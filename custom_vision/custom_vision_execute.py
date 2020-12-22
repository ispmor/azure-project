from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import pathlib
import time

import voc_converter
import config

def init_project(trainer: CustomVisionTrainingClient, project_name: str, domain_type: str, domain_name: str): # noqa
    obj_detection_domain = next(
        domain for domain in trainer.get_domains()
        if domain.type == domain_type and domain.name == domain_name
    )

    print("Creating project...")
    project = trainer.create_project(
        project_name, domain_id=obj_detection_domain.id
    )

    return project


def init_trainer() -> CustomVisionTrainingClient:
    credentials = ApiKeyCredentials(
        in_headers={"Training-key": config.TRAINING_KEY}
    )
    trainer = CustomVisionTrainingClient(config.ENDPOINT, credentials)
    return trainer


def init_predictor() -> CustomVisionPredictionClient:
    prediction_credentials = ApiKeyCredentials(
        in_headers={"Prediction-key": config.PREDICTION_KEY}
    )
    predictor = CustomVisionPredictionClient(
        config.ENDPOINT, prediction_credentials
    )
    return predictor


def create_tags(tags: list, trainer: CustomVisionTrainingClient, project) -> dict: # noqa
    tag_ids = {}
    for tag in tags:
        tag_ids[tag] = trainer.create_tag(project.id, tag)
    return tag_ids


def create_tagged_images(dataset_train_path: pathlib.Path, tag_ids: dict) -> list: # noqa
    print("Adding images...")
    tagged_images_with_regions = []

    for file in (dataset_train_path).rglob('*.jpg'):
        regions = voc_converter.get_regions_from_xml(
            file.with_suffix('.xml'), tag_ids
        )
        with open(file, mode="rb") as image_contents:
            tagged_images_with_regions.append(ImageFileCreateEntry(
                name=file.name, contents=image_contents.read(), regions=regions
            ))
    return tagged_images_with_regions


def upload_batches(trainer: CustomVisionTrainingClient, tagged_images_with_regions: list, project): # noqa
    for i in range(0, len(tagged_images_with_regions), config.CV_BATCH_SIZE):
        end = i + config.CV_BATCH_SIZE \
            if i + config.CV_BATCH_SIZE < len(tagged_images_with_regions) \
            else len(tagged_images_with_regions)
        upload_result = trainer.create_images_from_files(
            project.id, ImageFileCreateBatch(
                images=tagged_images_with_regions[i:end]
            )
        )
    # if not upload_result.is_batch_successful:
    #     print(i, end)
    #     print("Image batch upload failed.")
    #     print(len(upload_result.images))
    #     for image in upload_result.images:
    #         print("Image status: ", image.status)
    #     print(upload_result.status)
    #     exit(-1)
    return upload_result


def train(trainer: CustomVisionTrainingClient, project, publish_iteration_name: str, prediction_resource_id: str): # noqa
    print("Training...")
    iteration = trainer.train_project(project.id)
    while (iteration.status != "Completed"):
        iteration = trainer.get_iteration(project.id, iteration.id)
        print("Training status: " + iteration.status)
        time.sleep(1)

    trainer.publish_iteration(
        project.id, iteration.id, publish_iteration_name,
        prediction_resource_id
    )
    print("Done!")


def test(dataset_train_path: pathlib.Path, predictor: CustomVisionPredictionClient, project): # noqa
    results = []
    for file in (dataset_train_path).rglob('*.jpg'):
        with open(file, mode="rb") as test_data:
            results.append(predictor.detect_image(
                project.id, publish_iteration_name, test_data
            ))
    for result in results:
        for prediction in result.predictions:
            print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height)) # noqa


if __name__ == "__main__":
    tags = ['cat', 'dog', 'monkey']
    dataset_path = pathlib.Path('/home/jakub/Studia/Semestr7/azure/projekt/azure-project/data/archive/yolo-animal-detection-small') # noqa
    dataset_train_path = dataset_path / 'train/'
    dataset_test_path = dataset_path / 'test/'
    publish_iteration_name = "detectModel"

    trainer = init_trainer()
    predictor = init_predictor()
    project = init_project(
        trainer, 'Monkey, Cat, Dog Detection', 'ObjectDetection', 'General'
    )
    tag_ids = create_tags(tags, trainer, project)
    tagged_images_with_regions = create_tagged_images(
        dataset_train_path, tag_ids
    )
    upload_batches(trainer, tagged_images_with_regions, project)
    train(
        trainer, project, publish_iteration_name, config.PREDICTION_RESOURCE_ID
    )
    test(dataset_test_path, predictor, project)

