# Image-to-Image Translation for images featuring Gzhel and Khokhloma patterns

Implementation of CycleGAN based on the [original paper](https://arxiv.org/pdf/1703.10593).

![photo_2024-05-30_12-45-12](https://github.com/olyandrevn/CycleGAN/assets/33371372/3c9c95ad-6f6b-4755-9541-491b4281868a)

### Model Architecture

**Generator**: [ResNet Generator](https://github.com/olyandrevn/CycleGAN/blob/main/cyclegan/model/generator.py)

**Discriminator**: [PatchGAN](https://github.com/olyandrevn/CycleGAN/blob/main/cyclegan/model/discriminator.py)

### Experiments

The example of **experiment** setup can be found in this [notebook](https://github.com/olyandrevn/CycleGAN/blob/main/experiment.ipynb). The **checkpoint** can be loaded from [here](https://drive.google.com/file/d/1SVqnSiRnF99GAXi5o38jUh1LLNWiHQ8K/view?usp=sharing).


For the final training the following parameters were used:

```
lr = 2e-3
epochs = 40
batch_size = 10
lambda_value = 10.0
img_size = 128

step_size_lr = 10
gamma = 0.1

g_iters_per_epoch = 1
d_iters_per_epoch = 1

g_resnet_blocks = 6
d_layers = 3
```

## Dataset
The details of dataset collection can be found [here](https://github.com/olyandrevn/CycleGAN/blob/main/parser/README.md).

## Results

![Screenshot from 2024-05-30 12-48-00](https://github.com/olyandrevn/CycleGAN/assets/33371372/cbc0f311-e67d-41e6-a05a-ad7904d87fc0)
![Screenshot from 2024-05-30 12-48-28](https://github.com/olyandrevn/CycleGAN/assets/33371372/177e6ad2-8c4e-4ae5-b197-0587d79794c3)
