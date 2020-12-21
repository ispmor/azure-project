import xmltodict
import pathlib
from azure.cognitiveservices.vision.customvision.training.models import Region


def get_azure_region(voc_object: dict, w: int, h: int, tag_ids: dict) -> Region: # noqa
    voc_region = voc_object["bndbox"]
    tag = tag_ids[voc_object["name"]]

    left = float(voc_region['xmin']) / w
    top = float(voc_region['ymin']) / h
    width = (float(voc_region["xmax"]) - float(voc_region['xmin'])) / w
    height = (float(voc_region["ymax"]) - float(voc_region['ymin'])) / h

    return Region(
        tag_id=tag.id, left=left, top=top, width=width, height=height
    )


def get_regions_from_xml(xml_path: pathlib.Path, tag_ids: dict) -> list:
    regions = []

    with open(xml_path) as f:
        voc = xmltodict.parse(f.read())["annotation"]

    w = int(voc['size']['width'])
    h = int(voc['size']['height'])

    if type(voc['object']) == list:
        for voc_object in voc['object']:
            regions.append(get_azure_region(voc_object, w, h, tag_ids))  
    else:
        regions.append(get_azure_region(voc['object'], w, h, tag_ids))

    return regions


if __name__ == '__main__':
    xml_path = pathlib.Path('/home/jakub/Studia/Semestr7/azure/projekt/azure-project/data/archive/yolo-animal-detection-small/test/cats_000.xml') # noqa

    print(get_regions_from_xml(xml_path))
