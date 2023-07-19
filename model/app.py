import torch
import wandb
import albumentations as A

import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import CosineAnnealingLR
from importlib import import_module

from dataset import *
from models import *
from loss import *
from train import *
from utils import *


def main(args):
    """
    args : 기본적으로 가져와야할 매개변수를 argParser로 가져온다.
        dataset_path
        model_name
        seed
        num_workers
        epochs
        batch
        resize
        lr
        weight_decay
    """
    torch.cuda.empty_cache()
    set_seed(args.seed)
    wandb.init(project="final_project", name=f"cls_{args.model_name}")

    tf = A.Compose(
        [
            A.Resize(args.resize, args.resize),
            A.HorizontalFlip(),
            A.Normalize(),
        ]
    )
    train_dataset = CustomCombineDataset(
        "/opt/ml/level3_cv_finalproject-cv-01/model", is_train=True, tf=tf
    )
    valid_dataset = CustomCombineDataset(
        "/opt/ml/level3_cv_finalproject-cv-01/model",
        is_train=False,
        tf=tf,
    )
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=args.batch,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=custom_combine_collate_fn,
        drop_last=False,
    )
    valid_loader = DataLoader(
        dataset=valid_dataset,
        batch_size=args.batch,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=custom_combine_collate_fn,
        drop_last=False,
    )

    model_module = getattr(import_module("models"), args.model_name)
    model = model_module(num_classes=110)

    # criterion = [
    #     CLSLoss(num_classes=93, weight=[1, 0.1], smoothing=0.1),
    #     RCPLoss(num_classes=17, weight=[1, 0.2], smoothing=0.1, gamma=2.0),
    # ]
    criterion = AsymmetricLoss(
        gamma_neg=4,
        gamma_pos=0,
        clip=0.05,
        eps=1e-8,
        disable_torch_grad_focal_loss=True,
    )
    optimizer = optim.AdamW(
        params=model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=args.eta_min)

    # train(model, optimizer, criterion, scheduler, train_loader, valid_loader, args)
    combine_train(
        model, optimizer, criterion, scheduler, train_loader, valid_loader, args
    )
    wandb.finish()


if __name__ == "__main__":
    args = parse_args()
    main(args)
