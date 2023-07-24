import torch

from ml_decoder import add_ml_decoder_head
from timm.models import (
    resnet18,
    resnet50d,
    tresnet_m,
    tresnet_l,
    efficientnetv2_s,
    efficientnetv2_m,
    vit_tiny_r_s16_p8_384,
    vit_small_r26_s32_384,
    swinv2_cr_base_384,
    swinv2_cr_tiny_384,
)


class ResNet18(torch.nn.Module):
    def __init__(self, num_classes=93):
        super(ResNet18, self).__init__()
        self.model = resnet18(pretrained=True)
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.model(x)


class ResNet18_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(ResNet18_recipy, self).__init__()
        self.model = resnet18(pretrained=True)
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Identity()

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class ResNet50d_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(ResNet50d_recipy, self).__init__()
        self.model = resnet50d(pretrained=True)
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Identity()

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class Tresnet_m_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(Tresnet_m_recipy, self).__init__()
        self.model = tresnet_m(pretrained=True)
        num_features = self.model.head.fc.out_features

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class Tresnet_m_ml_decoder_recipy(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Tresnet_m_ml_decoder_recipy, self).__init__()
        self.model = add_ml_decoder_head(
            model=tresnet_m(pretrained=True), num_classes=num_classes
        )

    def forward(self, x):
        return self.model(x)


class Tresnet_l_ml_decoder_recipy(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Tresnet_l_ml_decoder_recipy, self).__init__()
        self.model = add_ml_decoder_head(
            model=tresnet_l(pretrained=True), num_classes=num_classes
        )

    def forward(self, x):
        return self.model(x)


class Efficientnetv2_s(torch.nn.Module):
    def __init__(self, num_classes=93):
        super(Efficientnetv2_s, self).__init__()
        self.model = efficientnetv2_s(pretrained=False)
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.model(x)


class Efficientnetv2_s_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(Efficientnetv2_s_recipy, self).__init__()
        self.model = efficientnetv2_s(pretrained=False)
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Identity()

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class Efficientnetv2_m(torch.nn.Module):
    def __init__(self, num_classes=93):
        super(Efficientnetv2_m, self).__init__()
        self.model = efficientnetv2_m(pretrained=False)
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.model(x)


class Efficientnetv2_m_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(Efficientnetv2_m_recipy, self).__init__()
        self.model = efficientnetv2_m(pretrained=False)
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Identity()
        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class Vit_tiny(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(Vit_tiny, self).__init__()
        self.model = vit_tiny_r_s16_p8_384(pretrained=True)
        num_features = self.model.head.out_features
        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class Vit_tiny_combine(torch.nn.Module):
    def __init__(self, num_classes=110):
        super(Vit_tiny_combine, self).__init__()
        self.model = vit_tiny_r_s16_p8_384(pretrained=True, num_classes=num_classes)

    def forward(self, x):
        return self.model(x)


class Vit_small(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(Vit_small, self).__init__()
        self.model = vit_small_r26_s32_384(pretrained=True)
        num_features = self.model.head.out_features
        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class swinv2_cr_tiny_384_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(swinv2_cr_tiny_384_recipy, self).__init__()
        self.model = swinv2_cr_tiny_384(pretrained=False)
        num_features = self.model.head.fc.out_features
        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output


class swinv2_cr_base_384_recipy(torch.nn.Module):
    def __init__(self, num_classes=93, num_allergy=17):
        super(swinv2_cr_base_384_recipy, self).__init__()
        self.model = swinv2_cr_base_384(pretrained=False)
        num_features = self.model.head.fc.out_features
        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_output = self.fc2(outputs)
        return cls_output, rcp_output
