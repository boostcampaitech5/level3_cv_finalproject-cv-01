import os
import cv2
import pandas as pd

from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, base_path, is_train=False, tf=None) -> None:
        df = pd.read_csv(os.path.join(base_path, "data/data.csv"))
        images_path = []
        labels = []
        for i, image_path, label in zip(df["class_id"], df["img_path"], df["label"]):
            if is_train and i > 200:
                images_path.append(os.path.join(base_path, image_path))
                labels.append(label)
            else:
                images_path.append(os.path.join(base_path, image_path))
                labels.append(label)

        self.classes = sorted(set(labels))
        self.cls2idx = {c: i for i, c in enumerate(self.classes)}
        self.images_path = images_path
        self.labels = labels
        self.is_train = is_train
        self.tf = tf

    def __len__(self):
        return len(self.images_path)

    def __getitem__(self, index):
        image_path = self.images_path[index]
        label = self.labels[index]
        image = cv2.imread(image_path)

        if self.tf is not None:
            inputs = {"image": image}
            result = self.tf(**inputs)

            image = result["image"]
        image.permute(2, 0, 1)
        return image, self.cls2idx[label]
