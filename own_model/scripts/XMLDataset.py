import os
import xml.etree.ElementTree as ET
import torch
import transforms as T
from PIL import Image


class BuildDataset(torch.utils.data.Dataset):
    def __init__(self, root, transforms=None, train=True):
        self.root = root
        self.transforms = transforms
        self.labels_dict = {'cat': 1, 'dog': 2, 'monkey': 3}
#         self.labels_dict['cat'] = 1
#         self.labels_dict['dog'] = 2
#         self.labels_dict['monkey'] = 3
        # load all image files
        if train:
            self.imgs_path = os.path.join(root, "Data/JPEGImages")
            self.imgs = list(sorted(os.listdir(self.imgs_path)))
            self.xmls_path = os.path.join(root, "Data/Annotations")
        else:
            self.imgs_path = os.path.join(root, "Data/JPEGImagesTest")
            self.imgs = list(sorted(os.listdir(self.imgs_path)))
            self.xmls_path = os.path.join(root, "Data/AnnotationsTest")

    def __getitem__(self, idx):
        img_path = os.path.join(self.imgs_path, self.imgs[idx])
        xml_path = os.path.join(
            self.xmls_path, "{}.xml".format(self.imgs[idx].strip(".jpg"))
        )
        img = Image.open(img_path).convert("RGB")

        # parse XML annotation
        tree = ET.parse(xml_path)
        t_root = tree.getroot()

        # get bounding box coordinates
        boxes = []
        labels = []
        for obj in t_root.findall("object"):
            bnd_box = obj.find("bndbox")
            xmin = float(bnd_box.find("xmin").text)
            xmax = float(bnd_box.find("xmax").text)
            ymin = float(bnd_box.find("ymin").text)
            ymax = float(bnd_box.find("ymax").text)
            boxes.append([xmin, ymin, xmax, ymax])
            label_name = str(obj.find("name").text)
#             if self.labels_dict:
#                 if label_name not in self.labels_dict.keys():
#                     self.labels_dict[label_name] = max(self.labels_dict.values()) + 1
#             else:
#                 self.labels_dict[label_name] = 1
#             print(label_name + ": " + str(self.labels_dict[label_name]))
            labels.append(self.labels_dict[label_name])
        num_objs = len(boxes)
        boxes = torch.as_tensor(boxes, dtype=torch.float32)

        # there is only one class
        labels = torch.as_tensor(labels)
#         print(labels)
#         labels = torch.ones((num_objs,), dtype=torch.int64)
        image_id = torch.tensor([idx])

        # area of the bounding box, used during evaluation with the COCO metric for small, medium and large boxes
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])

        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)


def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)
