import torch
import torch.nn as nn
import torch.nn.functional as F


class LabelSmoothingLoss(nn.Module):
    def __init__(self, num_classes, smoothing=0.0):
        super(LabelSmoothingLoss, self).__init__()
        assert 0 <= smoothing < 1
        self.smoothing = smoothing
        self.num_classes = num_classes

    def forward(self, pred, target):
        confidence = 1.0 - self.smoothing
        smoothing_value = self.smoothing / (self.num_classes - 1)

        target_one_hot = torch.full_like(pred, smoothing_value)
        target_one_hot.scatter_(1, target.to(torch.int64), confidence)

        log_probabilities = torch.log_softmax(pred, dim=1)

        loss = -torch.sum(target_one_hot * log_probabilities, dim=1)
        return torch.mean(loss)


class FocalLoss(nn.Module):
    def __init__(self, weight=None, gamma=2, reduction="mean"):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.reduction = reduction
        self.weight = weight  # weight parameter will act as the alpha parameter to balance class weights

    def forward(self, pred, target):
        ce_loss = F.binary_cross_entropy_with_logits(
            pred, target, reduction=self.reduction, weight=self.weight
        )
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma * ce_loss).mean()
        return focal_loss


class CombinationLoss(nn.Module):
    def __init__(self, num_classes, weight, smoothing=0.0, gamma=2.0) -> None:
        super(CombinationLoss, self).__init__()
        self.weight = weight
        self.bce = nn.BCEWithLogitsLoss()
        self.label_smoothing = LabelSmoothingLoss(num_classes, smoothing)
        self.focal = FocalLoss(gamma=gamma)

    def forward(self, pred, target):
        bce = self.bce(pred, target) * self.weight[0]
        label_smoothing = self.label_smoothing(pred, target) * self.weight[1]
        focal = self.focal(pred, target) * self.weight[2]
        return bce + label_smoothing + focal
