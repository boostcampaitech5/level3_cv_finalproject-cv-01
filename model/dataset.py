import os
import cv2
import json
import numpy as np
import pandas as pd

from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, base_path, is_train=False, tf=None) -> None:
        df = pd.read_csv(os.path.join(base_path, "data/data.csv"))
        images_path, jsons_path = [], []
        for i, image_path, json_path in zip(
            df["class_id"], df["img_path"], df["json_path"]
        ):
            if is_train and i > 200:
                images_path.append(os.path.join(base_path, image_path))
                jsons_path.append(os.path.join(base_path, json_path))
            else:
                images_path.append(os.path.join(base_path, image_path))
                jsons_path.append(os.path.join(base_path, json_path))

        with open(os.path.join(base_path, "data/ingredients.json")) as file:
            self.ingredients = json.load(file)
        self.igd2idx = {igd: int(i) for i, igd in self.ingredients.items()}

        with open(os.path.join(base_path, "data/classes.json")) as file:
            self.classes = json.load(file)
        self.cls2idx = {c: int(i) for i, c in self.classes.items()}

        self.images_path = images_path
        self.jsons_path = jsons_path
        self.is_train = is_train
        self.tf = tf

    def __len__(self):
        return len(self.images_path)

    def __getitem__(self, index):
        image_path = self.images_path[index]
        json_path = self.jsons_path[index]

        ## IMAGE 생성
        image = cv2.imread(image_path)
        with open(json_path) as file:
            data = json.load(file)

        ## Label 생성
        labels = np.zeros(len(self.classes))
        labels[self.cls2idx[data["food_class"]]] = 1
        # for label in data["food_class"]:
        #     label[self.cls2idx[label]] = 1

        ## Ingredient 생성
        ingredient = np.zeros(len(self.ingredients))
        for element in data["ingredients"]:
            ingredient[self.igd2idx[element["ingredient"]]] = 1

        if self.tf is not None:
            inputs = {"image": image}
            result = self.tf(**inputs)

            image = result["image"]
        image = image.transpose(2, 0, 1)
        return image, labels, ingredient
