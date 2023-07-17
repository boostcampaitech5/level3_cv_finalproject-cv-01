import torch

from timm.models import (
    resnet18,
    resnet50d,
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
