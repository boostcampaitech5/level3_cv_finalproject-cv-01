import random
import torch
import numpy as np

from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        "--dataset_path",
        type=str,
        default="/opt/ml/dataset",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="/opt/ml/level3_cv_finalproject-cv-01/model/save",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="ResNet18",
    )
    parser.add_argument("--seed", type=int, default=31)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch", type=int, default=64)
    parser.add_argument("--resize", type=int, default=224)
    parser.add_argument("--lr", type=float, default=1e-2)
    parser.add_argument("--weight_decay", type=float, default=1e-3)

    args = parser.parse_args()
    print(args)
    return args


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)


def custom_collate_fn(sample):
    img, label, igd = list(zip(*sample))
    img = np.array(img, dtype=np.float32)
    label = np.array(label, dtype=np.float32)
    igd = np.array(igd, dtype=np.float32)
    return img, label, igd
