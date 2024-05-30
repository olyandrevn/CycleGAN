from cyclegan.model.blocks import *

class ResNetGenerator(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, n_filters=64, n_blocks=6, n_downsample=2):
        """
        Args:
          in_channels (int):  Number of input channels.
          out_channels (int): Number of output channels.
          n_blocks (int): Number of ResidualBlocks.
        """
        super(ResNetGenerator, self).__init__()

        model = [nn.ReflectionPad2d(3),
                 ConvBlock(in_channels=in_channels, out_channels=n_filters, kernel_size=7, padding=0),
                 nn.ReLU()]

        model += self._downsampling(n_filters=n_filters, n_downsample=n_downsample)

        model += self._add_residual_blocks(n_filters=n_filters, n_blocks=n_blocks, n_downsample=n_downsample)

        model += self._upsampling(n_filters=n_filters, n_upsample=n_downsample)

        model += [nn.ReflectionPad2d(3),
                  ConvBlock(in_channels=n_filters, out_channels=out_channels, kernel_size=7, padding=0),
                  nn.Tanh()]

        self.model = nn.Sequential(*model)

    def _downsampling(self, n_filters, n_downsample):
        downsample_blocks = []
        for i in range(n_downsample):
            filter_mul = 2 ** i
            in_channels = n_filters * filter_mul
            out_channels = n_filters * filter_mul * 2

            downsample_blocks += [ConvBlock(in_channels=in_channels, out_channels=out_channels),
                                  nn.ReLU()]

        return downsample_blocks

    def _add_residual_blocks(self, n_filters, n_blocks, n_downsample):
        res_blocks = []
        filter_mul = 2 ** n_downsample

        for i in range(n_blocks):
            res_blocks += [ResidualBlock(n_filters*filter_mul)]

        return res_blocks

    def _upsampling(self, n_filters, n_upsample):
        upsample_blocks = []
        for i in range(n_upsample):
            filter_mul = 2 ** (n_upsample - i)
            in_channels = n_filters * filter_mul
            out_channels = n_filters * filter_mul // 2

            upsample_blocks += [ConvBlock(in_channels=in_channels, out_channels=out_channels, frac_stride=True),
                                nn.ReLU()]

        return upsample_blocks

    def forward(self, x):
        return self.model(x)
