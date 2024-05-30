import os
import wandb
import warnings
import torch
from collections import defaultdict
from termcolor import colored
from pathlib import Path

import matplotlib.pyplot as plt

def get_model_name(chkp_folder, model_name=None):
    if model_name is None:
        if os.path.exists(chkp_folder):
            num_starts = len(os.listdir(chkp_folder)) + 1
        else:
            num_starts = 1
        model_name = f'model.{num_starts}'
    else:
        if "." not in model_name:
            model_name += ".0"
    changed = False
    while os.path.exists(os.path.join(chkp_folder, model_name + '.pt')):
        model_name, ind = model_name.split(".")
        model_name += f".{int(ind) + 1}"
        changed=True
    if changed:
        warnings.warn(f"Selected model_name was used already! To avoid possible overwrite - model_name changed to {model_name}")
    return model_name


def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def save_model(epoch, name, model):
    artifact = wandb.Artifact(name, type='model', metadata=dict(epochs=epoch))
    model_path = os.path.join('model', name+'_epoch-{}.pth'.format(epoch))
    Path('model').mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_path)
    artifact.add_file(model_path)
    wandb.log_artifact(artifact)

def draw_imgs(model, num_images, loader_a, loader_b, de_norm_a, de_norm_b, device='cuda'):
    model.eval()
    with torch.no_grad():
        imgs_a = next(iter(loader_a))[:num_images].to(device)
        imgs_b = next(iter(loader_b))[:num_images].to(device)

        fake_a = model.G_BA(imgs_b)
        fake_b = model.G_AB(imgs_a)

        rec_a = model.G_BA(fake_b)
        rec_b = model.G_AB(fake_a)

        # Log images from A
        table_a = wandb.Table(columns=["Original from A", "Translated to B", "Reconstructed A"])
        for ind in range(num_images):
            orig_a = de_norm_a(imgs_a[ind], normalized=True)
            trans_b = de_norm_b(fake_b[ind], normalized=True)
            recon_a = de_norm_a(rec_a[ind], normalized=True)

            table_a.add_data(
                wandb.Image(orig_a, caption="Original from A"),
                wandb.Image(trans_b, caption="Translated to B"),
                wandb.Image(recon_a, caption="Reconstructed A")
            )
        wandb.log({"Images from A": table_a})

        # Log images from B
        table_b = wandb.Table(columns=["Original from B", "Translated to A", "Reconstructed B"])
        for ind in range(num_images):
            orig_b = de_norm_b(imgs_b[ind], normalized=True)
            trans_a = de_norm_a(fake_a[ind], normalized=True)
            recon_b = de_norm_b(rec_b[ind], normalized=True)

            table_b.add_data(
                wandb.Image(orig_b, caption="Original from B"),
                wandb.Image(trans_a, caption="Translated to A"),
                wandb.Image(recon_b, caption="Reconstructed B")
            )
        wandb.log({"Images from B": table_b})

def beautiful_int(i):
    i = str(i)
    return ".".join(reversed([i[max(j, 0):j+3] for j in range(len(i) - 3, -3, -3)]))


def model_num_params(model, verbose_all=False, verbose_only_learnable=False):
    sum_params = 0
    sum_learnable_params = 0
    submodules = defaultdict(lambda : [0, 0])
    for name, param in model.named_parameters():
        num_params = param.numel()
        if verbose_all or (verbose_only_learnable and param.requires_grad):
            print(
                colored(
                    '{: <65} ~  {: <9} params ~ grad: {}'.format(
                        name,
                        beautiful_int(num_params),
                        param.requires_grad,
                    ),
                    {True: "green", False: "red"}[param.requires_grad],
                )
            )
        sum_params += num_params
        sm = name.split(".")[0]
        submodules[sm][0] += num_params
        if param.requires_grad:
            sum_learnable_params += num_params
            submodules[sm][1] += num_params
    print(
        f'\nIn total:\n  - {beautiful_int(sum_params)} params\n  - {beautiful_int(sum_learnable_params)} learnable params'
    )

    for sm, v in submodules.items():
        print(
            f"\n . {sm}:\n .   - {beautiful_int(submodules[sm][0])} params\n .   - {beautiful_int(submodules[sm][1])} learnable params"
        )
    return sum_params, sum_learnable_params

def display_image_pairs(dataset, model, num_images, de_normalize_a, de_normalize_b, device='cuda', dataset_type='A'):
    """
    Display pairs of images from the dataset and their corresponding generated images.

    Parameters:
    - dataset: The dataset containing the images.
    - model: The model used to generate the images.
    - num_images: The number of image pairs to display.
    - device: The device to run the model on (e.g., 'cpu' or 'cuda').

    """
    fig, axes = plt.subplots(num_images, 2, figsize=(5, 2 * num_images))

    for i in range(num_images):
        img_ind = i
        if dataset_type == 'A':
            img_a = dataset.test_a[img_ind].to(device).unsqueeze(0)
            fake_b = model.G_AB(img_a)

            axes[i, 0].imshow(de_normalize_a(img_a[0]))
            axes[i, 0].axis('off')

            axes[i, 1].imshow(de_normalize_b(fake_b[0]))
            axes[i, 1].axis('off')
        else:
            img_b = dataset.test_b[img_ind].to(device).unsqueeze(0)
            fake_a = model.G_BA(img_b)

            axes[i, 0].imshow(de_normalize_b(img_b[0]))
            axes[i, 0].axis('off')

            axes[i, 1].imshow(de_normalize_a(fake_a[0]))
            axes[i, 1].axis('off')

    plt.show()