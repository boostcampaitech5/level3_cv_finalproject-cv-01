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


class AsymmetricLoss(nn.Module):
    def __init__(
        self,
        gamma_neg=4,
        gamma_pos=0,
        clip=0.05,
        eps=1e-8,
        disable_torch_grad_focal_loss=True,
    ):
        super(AsymmetricLoss, self).__init__()

        self.gamma_neg = gamma_neg
        self.gamma_pos = gamma_pos
        self.clip = clip
        self.disable_torch_grad_focal_loss = disable_torch_grad_focal_loss
        self.eps = eps

    def forward(self, x, y):
        """ "
        Parameters
        ----------
        x: input logits
        y: targets (multi-label binarized vector)
        """

        # Calculating Probabilities
        x_sigmoid = torch.sigmoid(x)
        xs_pos = x_sigmoid
        xs_neg = 1 - x_sigmoid

        # Asymmetric Clipping
        if self.clip is not None and self.clip > 0:
            xs_neg = (xs_neg + self.clip).clamp(max=1)

        # Basic CE calculation
        los_pos = y * torch.log(xs_pos.clamp(min=self.eps))
        los_neg = (1 - y) * torch.log(xs_neg.clamp(min=self.eps))
        loss = los_pos + los_neg

        # Asymmetric Focusing
        if self.gamma_neg > 0 or self.gamma_pos > 0:
            if self.disable_torch_grad_focal_loss:
                torch.set_grad_enabled(False)
            pt0 = xs_pos * y
            pt1 = xs_neg * (1 - y)  # pt = p if t > 0 else 1-p
            pt = pt0 + pt1
            one_sided_gamma = self.gamma_pos * y + self.gamma_neg * (1 - y)
            one_sided_w = torch.pow(1 - pt, one_sided_gamma)
            if self.disable_torch_grad_focal_loss:
                torch.set_grad_enabled(True)
            loss *= one_sided_w

        return -loss.sum()


class CLSLoss(nn.Module):
    def __init__(self, num_classes, weight, smoothing=0.0, gamma=2.0) -> None:
        super(CLSLoss, self).__init__()
        self.weight = weight
        self.bce = nn.BCEWithLogitsLoss()
        self.label_smoothing = LabelSmoothingLoss(num_classes, smoothing)

    def forward(self, pred, target):
        bce = self.bce(pred, target) * self.weight[0]
        label_smoothing = self.label_smoothing(pred, target) * self.weight[1]
        return bce + label_smoothing


class RCPLoss(nn.Module):
    def __init__(self, num_classes, weight, smoothing=0.0, gamma=2.0) -> None:
        super(RCPLoss, self).__init__()
        self.weight = weight
        self.bce = nn.BCEWithLogitsLoss()
        # self.label_smoothing = LabelSmoothingLoss(num_classes, smoothing)
        self.focal = FocalLoss(gamma=gamma)

    def forward(self, pred, target):
        bce = self.bce(pred, target) * self.weight[0]
        # label_smoothing = self.label_smoothing(pred, target) * self.weight[1]
        focal = self.focal(pred, target) * self.weight[1]
        # return bce + label_smoothing + focal
        return bce + focal
