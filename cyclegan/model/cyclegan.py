from cyclegan.model.generator import *
from cyclegan.model.discriminator import *

class CycleGAN(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, n_filters=64, n_blocks=6, n_downsample=2, n_layers=3):
        super(CycleGAN, self).__init__()
        self.G_AB = ResNetGenerator(in_channels=in_channels, out_channels=out_channels, n_filters=n_filters, n_blocks=n_blocks, n_downsample=n_downsample)
        self.G_BA = ResNetGenerator(in_channels=in_channels, out_channels=out_channels, n_filters=n_filters, n_blocks=n_blocks, n_downsample=n_downsample)

        self.D_A = PatchGAN(in_channels=in_channels, n_filters=n_filters, n_layers=n_layers)
        self.D_B = PatchGAN(in_channels=in_channels, n_filters=n_filters, n_layers=n_layers)

    def to(self, device):
        self.G_AB.to(device)
        self.G_BA.to(device)
        self.D_A.to(device)
        self.D_B.to(device)
