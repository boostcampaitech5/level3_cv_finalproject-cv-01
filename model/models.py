import torch

from timm.models import resnet18, efficientnetv2_s


class ResNet18(torch.nn.Module):
    def __init__(self, num_classes=93):
        super(ResNet18, self).__init__()
        self.model = resnet18(pretrained=True)
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(num_features, num_classes)

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
