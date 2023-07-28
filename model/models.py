import torch

from ml_decoder import add_ml_decoder_head
from timm.models import (
    resnet50d,
    tresnet_m,
    efficientnetv2_s,
    vit_tiny_r_s16_p8_384,
    vit_small_r26_s32_384,
    swinv2_cr_tiny_384,
)


class ResNet50d_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(ResNet50d_combine, self).__init__()
        self.model = resnet50d(pretrained=True, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)


class Tresnet_m_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Tresnet_m_combine, self).__init__()
        self.model = tresnet_m(pretrained=True, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)


class Tresnet_m_ml_decoder_recipy(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Tresnet_m_ml_decoder_recipy, self).__init__()
        self.model = add_ml_decoder_head(
            model=tresnet_m(pretrained=True), num_classes=num_classes
        )

    def forward(self, x):
        return self.model(x)


class Efficientnetv2_s_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Efficientnetv2_s_combine, self).__init__()
        self.model = efficientnetv2_s(pretrained=False, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)


class Vit_tiny_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Vit_tiny_combine, self).__init__()
        self.model = vit_tiny_r_s16_p8_384(pretrained=True, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)


class Vit_small_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Vit_small_combine, self).__init__()
        self.model = vit_small_r26_s32_384(pretrained=True, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)


class swinv2_cr_tiny_384_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(swinv2_cr_tiny_384_combine, self).__init__()
        self.model = swinv2_cr_tiny_384(pretrained=False, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)
