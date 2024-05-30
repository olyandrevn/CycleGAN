from cyclegan.model.blocks import *

class PatchGAN(nn.Module):
    def __init__(self, in_channels=3, n_filters=64, n_layers=3):
        """
        Args:
          in_channels (int):  Number of input channels.
          out_channels (int): Number of output channels.
          n_blocks (int): Number of ResidualBlocks.
        """
        super(PatchGAN, self).__init__()

        model = [nn.Conv2d(in_channels=in_channels, out_channels=n_filters, kernel_size=4, stride=2),
                 nn.LeakyReLU(0.2)]

        model += self._add_layers(n_filters=n_filters, n_layers=n_layers)

        filter_mul = min(2 ** n_layers, 8)
        in_channels = n_filters * filter_mul
        out_channels = n_filters * min(filter_mul * 2, 8)

        model += [ConvBlock(in_channels=in_channels, out_channels=out_channels, kernel_size=4, stride=1),
                  nn.LeakyReLU(0.2),
                  nn.Conv2d(out_channels, 1, kernel_size=4, stride=1, padding=1),
                  nn.AdaptiveAvgPool2d(1),
                  nn.Flatten()]

        self.model = nn.Sequential(*model)

    def _add_layers(self, n_filters, n_layers):
        layers = []
        for i in range(n_layers):  # gradually increase the number of filters
            filter_mul = min(2 ** i, 8)
            in_channels = n_filters * filter_mul
            out_channels = n_filters * min(filter_mul * 2, 8)

            layers += [ConvBlock(in_channels=in_channels, out_channels=out_channels, kernel_size=4, stride=2),
                       nn.LeakyReLU(0.2)]

        return layers

    def forward(self, x):
        return self.model(x)
