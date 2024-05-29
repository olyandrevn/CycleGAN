from cyclegan.dataset.dataset import *
from cyclegan.dataset.utils import *

def prepare_dataset(target_folder, batch_size):
    datasets = DatasetsClass(
        train_a=ImageDatasetNoLabel(os.path.join(target_folder, "trainA")),
        train_b=ImageDatasetNoLabel(os.path.join(target_folder, "trainB")),
        test_a=ImageDatasetNoLabel(os.path.join(target_folder, "testA")),
        test_b=ImageDatasetNoLabel(os.path.join(target_folder, "testB")),
    )

    channel_mean_a, channel_std_a = get_channel_statistics(datasets.train_a)
    channel_mean_b, channel_std_b = get_channel_statistics(datasets.train_b)


    hyperparams = dict()

    train_transform_a, val_transform_a, de_normalize_a = get_transforms(channel_mean_a, channel_std_a, **hyperparams)
    train_transform_b, val_transform_b, de_normalize_b = get_transforms(channel_mean_b, channel_std_b, **hyperparams)

    datasets = DatasetsClass(
        train_a=ImageDatasetNoLabel(
            os.path.join(target_folder, "trainA"),
            transforms=train_transform_a,
        ),
        train_b=ImageDatasetNoLabel(
            os.path.join(target_folder, "trainB"),
            transforms=train_transform_b,
        ),
        test_a=ImageDatasetNoLabel(
            os.path.join(target_folder, "testA"),
            transforms=val_transform_a,
        ),
        test_b=ImageDatasetNoLabel(
            os.path.join(target_folder, "testB"),
            transforms=val_transform_b,
        ),
    )

    dataloaders = DataLoadersClass(
        train_a=DataLoader(
            dataset=datasets.train_a,
            batch_size=batch_size,
            num_workers=4,
            shuffle=True,
            drop_last=True,
        ),
        train_b=DataLoader(
            dataset=datasets.train_b,
            batch_size=batch_size,
            num_workers=4,
            shuffle=True,
            drop_last=True,
        ),
        test_a=DataLoader(
            dataset=datasets.test_a,
            batch_size=batch_size,
            num_workers=4,
            shuffle=False,
            drop_last=True,
        ),
        test_b=DataLoader(
            dataset=datasets.test_b,
            batch_size=batch_size,
            num_workers=4,
            shuffle=False,
            drop_last=True,
        ),
    )

    return datasets, dataloaders, de_normalize_a, de_normalize_b
