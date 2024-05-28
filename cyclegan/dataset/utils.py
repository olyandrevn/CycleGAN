import torch
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2

def get_channel_statistics(dataset):
    pixel_list = [image.reshape(-1, 3)/255 for image in dataset.images]
    pixels = np.vstack(pixel_list)
    channel_mean = np.mean(pixels, axis=0)
    channel_std = np.std(pixels, axis=0)

    return channel_mean, channel_std

def get_transforms(mean, std):
    train_transform = A.Compose([
        A.ShiftScaleRotate(shift_limit=0.35, scale_limit=0.35, rotate_limit=5, p=0.3),
        A.Normalize(mean=mean, std=std),
        ToTensorV2(),
    ])

    val_transform = A.Compose([
        A.Normalize(mean=mean, std=std),
        ToTensorV2(),
    ])

    def de_normalize(img, normalized=True):
        if isinstance(img, torch.Tensor):
            img = img.detach().cpu().numpy()

        mean_array = np.array(mean).reshape(3, 1, 1)
        std_array = np.array(std).reshape(3, 1, 1)

        denorm_img = img * std_array + mean_array
        denorm_img = np.clip(denorm_img, 0, 1)

        return np.transpose(denorm_img, (1, 2, 0))
    return train_transform, val_transform, de_normalize
