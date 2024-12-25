import torch.nn as nn


# ------------------------------------------------------------
# 定义要训练的残差网络
# ------------------------------------------------------------
class ResBlock(nn.Module):
    def __init__(self, ch_in, ch_out, stride = 1):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size = 3, stride = stride, padding = 1),
            nn.BatchNorm2d(ch_out),
            nn.ReLU(),
            nn.Conv2d(ch_out, ch_out, kernel_size = 3, stride = 1, padding = 1),
            nn.BatchNorm2d(ch_out)
        )
        self.shortcut = nn.Sequential()
        if ch_in != ch_out:
            self.shortcut = nn.Sequential(
                nn.Conv2d(ch_in, ch_out, kernel_size = 1, stride = stride),
                nn.BatchNorm2d(ch_out)
            )

    def forward(self, x):
        out = self.conv(x) + self.shortcut(x)
        out = nn.functional.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.module = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size = 3, stride = 3, padding = 0),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            ResBlock(16, 32, stride = 3),
            ResBlock(32, 64, stride = 3),
            nn.AdaptiveMaxPool2d(1),
            nn.Flatten(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        out = self.module(x)
        return out
