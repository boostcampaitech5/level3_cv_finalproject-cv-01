import torch
import wandb
import albumentations as A

import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import CosineAnnealingLR

from dataset import *
from models import *
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
        lr
        weight_decay
    """
    torch.cuda.empty_cache()
    set_seed(args.seed)
    # wandb.init(project="final_project", name=f"cls_{args.model_name}")

    tf = A.Compose(
        [
            A.Resize(512, 512),
            A.Normalize(
                mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)
            ),  # Image net참고, 0을 기준으로 1의 표준편차
        ]
    )
    train_dataset = CustomDataset(
        "/opt/ml/level3_cv_finalproject-cv-01/model", is_train=True, tf=tf
    )
    valid_dataset = CustomDataset(
        "/opt/ml/level3_cv_finalproject-cv-01/model",
        is_train=False,
        tf=tf,
    )
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=args.batch,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=custom_collate_fn,
        drop_last=False,
    )
    valid_loader = DataLoader(
        dataset=valid_dataset,
        batch_size=args.batch,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=custom_collate_fn,
        drop_last=False,
    )

    model = ResNet18(num_classes=93)
    criterion = nn.CrossEntropyLoss()
    # criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.AdamW(
        params=model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-4)
    train(model, optimizer, criterion, scheduler, train_loader, valid_loader, args)
    # wandb.finish()


if __name__ == "__main__":
    args = parse_args()
    main(args)
