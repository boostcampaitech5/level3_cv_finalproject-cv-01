import os
import torch

import wandb
import datetime

from tqdm.auto import tqdm
from sklearn.metrics import f1_score

import torch.nn.functional as F


def validation(model, criterion, valid_loader):
    print("Start Validation...")
    model.eval()
    with torch.no_grad():
        total_loss, scores = [], []
        model.cuda()
        for images, labels in tqdm(valid_loader, total=len(valid_loader)):
            images = images.cuda()
            labels = torch.tensor(labels).cuda()

            outputs = model(images)
            labels = labels.long()
            loss = criterion(outputs, labels)

            outputs = F.softmax(outputs, dim=1)
            outputs = torch.argmax(outputs, dim=1)
            score = f1_score(y_true=labels.cpu(), y_pred=outputs.cpu(), average="macro")

            total_loss.append(loss)
            scores.append(score)
        mean_loss = torch.mean(torch.stack(total_loss))
        mean_score = sum(scores) / len(scores)
        return mean_loss, mean_score


def train(model, optimizer, criterion, scheduler, train_loader, valid_loader, args):
    print("Start Train...")

    scaler = torch.cuda.amp.GradScaler(enabled=True)
    best_score = 0
    model.cuda()
    for epoch in range(args.epochs):
        cur_time = datetime.datetime.now()
        model.train()
        for images, labels in train_loader:
            images, labels = (
                torch.tensor(images).cuda(),
                torch.tensor(labels).cuda(),
            )
            optimizer.zero_grad()

            with torch.cuda.amp.autocast(enabled=True):
                outputs = model(images)
                # outputs = F.softmax(outputs, dim=1)
                labels = labels.long()
                loss = criterion(outputs, labels)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            current_lr = optimizer.param_groups[0]["lr"]
            wandb.log({"train/LR": current_lr, "train/loss": loss})

        print(
            f"Duration :{datetime.datetime.now() - cur_time} |"
            f"Epoch [{epoch+1}/{args.epochs}], "
            f"Loss: {round(loss.item(),4)}"
        )

        wandb.log({"train/Epoch": epoch + 1})
        scheduler.step()

        loss, score = validation(model, criterion, valid_loader)

        print(f"Validation Marco-F1 Score : {score}")
        wandb.log({"val/Loss": loss, "val/Score": score})

        if score > best_score:
            best_score = score
            output_path = os.path.join(args.save_path, f"{args.model_name}_best.pth")
            torch.save(model, output_path)
        output_path = os.path.join(args.save_path, f"{args.model_name}_latest.pth")
        torch.save(model, output_path)
    print("Finish Train!!!")
