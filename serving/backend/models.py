import torch

from ml_decoder import add_ml_decoder_head
from timm.models import tresnet_m

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