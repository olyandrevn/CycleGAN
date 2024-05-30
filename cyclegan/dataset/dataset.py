import os
import cv2
import numpy as np

from torch.utils.data import Dataset, DataLoader
from dataclasses import dataclass

class ImageDatasetNoLabel(Dataset):
    def __init__(self, data_folder, transforms=None):
        super(ImageDatasetNoLabel).__init__()
        self.images = self.load_images(data_folder)
        self.transforms = transforms

    def load_images(self, data_folder):
        images = []
        for img_path in os.listdir(data_folder):
            img_path = os.path.join(data_folder, img_path)
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (128, 128))
            images.append(img)

        return images

    def __getitem__(self, index):
        img = self.images[index].astype(np.uint8)
        if self.transforms is not None:
            img = self.transforms(image=img)["image"]
        return img

    def __len__(self):
        return len(self.images)

@dataclass
class DatasetsClass:
    train_a: ImageDatasetNoLabel
    train_b: ImageDatasetNoLabel
    test_a: ImageDatasetNoLabel
    test_b: ImageDatasetNoLabel

@dataclass
class DataLoadersClass:
    train_a: DataLoader
    train_b: DataLoader
    test_a: DataLoader
    test_b: DataLoader
