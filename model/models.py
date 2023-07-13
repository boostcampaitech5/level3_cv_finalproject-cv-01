import torch

from timm.models import (
    resnet18,
    efficientnetv2_s,
    vit_small_r26_s32_224,
    efficientnetv2_m,
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
    def __init__(self, num_classes=93, num_allergy_map=100, num_allergy=17):
        super(ResNet18_recipy, self).__init__()
        self.model = resnet18(pretrained=True)
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Identity()

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy_map)
        self.last_fc = torch.nn.Linear(num_classes + num_allergy_map, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_feature = self.fc2(outputs)
        concat_output = torch.cat((cls_output, rcp_feature), dim=1)
        rcp_output = self.last_fc(concat_output)
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
    def __init__(self, num_classes=93, num_allergy_map=100, num_allergy=17):
        super(Efficientnetv2_s_recipy, self).__init__()
        self.model = efficientnetv2_s(pretrained=False)
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Identity()

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy_map)
        self.last_fc = torch.nn.Linear(num_classes + num_allergy_map, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_feature = self.fc2(outputs)
        concat_output = torch.cat((cls_output, rcp_feature), dim=1)
        rcp_output = self.last_fc(concat_output)
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
    def __init__(self, num_classes=93, num_allergy_map=100, num_allergy=17):
        super(Efficientnetv2_m_recipy, self).__init__()
        self.model = efficientnetv2_m(pretrained=False)
        num_features = self.model.classifier.in_features
        self.model.classifier = torch.nn.Identity()

        self.fc1 = torch.nn.Linear(num_features, num_classes)
        self.fc2 = torch.nn.Linear(num_features, num_allergy_map)
        self.last_fc = torch.nn.Linear(num_classes + num_allergy_map, num_allergy)

    def forward(self, x):
        outputs = self.model(x)
        cls_output = self.fc1(outputs)
        rcp_feature = self.fc2(outputs)
        concat_output = torch.cat((cls_output, rcp_feature), dim=1)
        rcp_output = self.last_fc(concat_output)
        return cls_output, rcp_output


class Vit_small(torch.nn.Module):
    def __init__(self, num_classes=93):
        super(Vit_small, self).__init__()
        self.model = vit_small_r26_s32_224(pretrained=True)
        num_features = self.model.head.out_features
        self.fc = torch.nn.Linear(num_features, num_classes)

    def forward(self, x):
        output = self.model(x)
        return self.fc(output)
