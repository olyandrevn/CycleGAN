import torch.nn as nn

class ConvBlock(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, kernel_size=3, padding=1, stride=1, frac_stride=False):
        """
        Args:
          in_channels (int):  Number of input channels.
          out_channels (int): Number of output channels.
        """
        super(ConvBlock, self).__init__()

        if frac_stride:
            self.block = nn.Sequential(
                nn.ConvTranspose2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, padding=padding, stride=stride),
                nn.InstanceNorm2d(out_channels))
        else:
            self.block = nn.Sequential(
                nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, padding=padding, stride=stride),
                nn.InstanceNorm2d(out_channels))

    def forward(self, x):
        out = self.block(x)
        return out

class ResidualBlock(nn.Module):
    def __init__(self, in_channels=3):
        """
        Args:
          in_channels (int):  Number of input channels.
        """
        super(ResidualBlock, self).__init__()

        self.conv_block1 = ConvBlock(in_channels, in_channels)
        self.conv_block2 = ConvBlock(in_channels, in_channels)

        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.conv_block1(x)
        out = self.relu(out)
        out = self.conv_block2(x)

        out = self.relu(x + out)
        return out
