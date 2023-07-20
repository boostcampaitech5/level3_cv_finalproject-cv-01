import os
import torch

import wandb
import datetime

from tqdm.auto import tqdm
from sklearn.metrics import f1_score, precision_score

import torch.nn.functional as F


def validation(model, criterion, valid_loader):
    print("Start Validation...")
    model.eval()
    with torch.no_grad():
        total_cls_loss, total_rcp_loss = [], []
        cls_f1_scores, rcp_f1_scores = [], []
        cls_precision_scores, rcp_precision_scores = [], []
        cls_thr, rcp_thr = 0.5, 0.5
        model.cuda()

        for images, labels, ingredients in tqdm(valid_loader, total=len(valid_loader)):
            images, labels, ingredients = (
                torch.tensor(images).cuda(),
                torch.tensor(labels).cuda(),
                torch.tensor(ingredients).cuda(),
            )
            cls_output, rcp_output = model(images)
            cls_loss = criterion[0](cls_output, labels)
            rcp_loss = criterion[1](rcp_output, ingredients)
            total_cls_loss.append(cls_loss)
            total_rcp_loss.append(rcp_loss)

            cls_output = F.sigmoid(cls_output)
            rcp_output = F.sigmoid(rcp_output)
            cls_output = (cls_output >= cls_thr).float()
            rcp_output = (rcp_output >= rcp_thr).float()
            cls_f1 = f1_score(
                y_pred=cls_output.cpu(),
                y_true=labels.cpu(),
                average="macro",
                zero_division=0,
            )
            rcp_f1 = f1_score(
                y_pred=rcp_output.cpu(),
                y_true=ingredients.cpu(),
                average="macro",
                zero_division=0,
            )
            cls_precision = precision_score(
                y_pred=cls_output.cpu(),
                y_true=labels.cpu(),
                average="macro",
                zero_division=0,
            )
            rcp_precision = precision_score(
                y_pred=rcp_output.cpu(),
                y_true=ingredients.cpu(),
                average="macro",
                zero_division=0,
            )
            cls_f1_scores.append(cls_f1)
            rcp_f1_scores.append(rcp_f1)
            cls_precision_scores.append(cls_precision)
            rcp_precision_scores.append(rcp_precision)
        mean_cls_loss = torch.mean(torch.stack(total_cls_loss))
        mean_rcp_loss = torch.mean(torch.stack(total_rcp_loss))
        mean_cls_f1_score = sum(cls_f1_scores) / len(cls_f1_scores)
        mean_rcp_f1_score = sum(rcp_f1_scores) / len(rcp_f1_scores)
        mean_cls_precision_scores = sum(cls_precision_scores) / len(
            cls_precision_scores
        )
        mean_rcp_precision_scores = sum(rcp_precision_scores) / len(
            rcp_precision_scores
        )
        return [mean_cls_loss, mean_rcp_loss], [
            mean_cls_f1_score,
            mean_rcp_f1_score,
            mean_cls_precision_scores,
            mean_rcp_precision_scores,
        ]


def train(model, optimizer, criterion, scheduler, train_loader, valid_loader, args):
    print("Start Train...")

    scaler = torch.cuda.amp.GradScaler(enabled=True)
    best_cls_f1_score, best_rcp_f1_score = 0, 0
    model.cuda()
    for epoch in range(args.epochs):
        cur_time = datetime.datetime.now()
        model.train()
        for images, labels, ingredients in train_loader:
            images, labels, ingredients = (
                torch.tensor(images).cuda(),
                torch.tensor(labels).cuda(),
                torch.tensor(ingredients).cuda(),
            )
            optimizer.zero_grad()

            with torch.cuda.amp.autocast(enabled=True):
                cls_output, rcp_output = model(images)
                cls_loss = criterion[0](cls_output, labels)
                rcp_loss = criterion[1](rcp_output, ingredients)
            scaler.scale(rcp_loss).backward(retain_graph=True)
            scaler.scale(cls_loss).backward()
            scaler.step(optimizer)
            scaler.update()

            current_lr = optimizer.param_groups[0]["lr"]
            wandb.log(
                {
                    "train/LR": current_lr,
                    "train/cls_loss": cls_loss,
                    "train/rcp_loss": rcp_loss,
                }
            )

        print(
            f"Duration :{datetime.datetime.now() - cur_time} |"
            f"Epoch [{epoch+1}/{args.epochs}], "
            f"CLS_loss: {round(cls_loss.item(),4)}, "
            f"RCP_loss: {round(rcp_loss.item(),4)}"
        )

        wandb.log({"train/Epoch": epoch + 1})
        scheduler.step()

        loss, score = validation(model, criterion, valid_loader)

        print(
            f"Validation CLS Marco F1 Score : {score[0]}\tValidation RCP Marco F1 Score : {score[1]}\n"
            f"Validation CLS Marco Precision Score : {score[2]}\tValidation RCP Marco Precision Score : {score[3]}\n"
        )
        wandb.log(
            {
                "val/cls_loss": loss[0],
                "val/rcp_loss": loss[1],
                "val/cls_F1-Score": score[0],
                "val/rcp_F1-Score": score[1],
                "val/cls_Precision-Score": score[2],
                "val/rcp_Precision-Score": score[3],
            }
        )

        if score[0] > best_cls_f1_score and score[1] > best_rcp_f1_score:
            best_cls_f1_score = score[0]
            best_rcp_f1_score = score[1]
            output_path = os.path.join(args.save_path, f"{args.model_name}_best.pth")
            torch.save(model, output_path)
        output_path = os.path.join(args.save_path, f"{args.model_name}_latest.pth")
        torch.save(model, output_path)
    print("Finish Train!!!")


def combine_validation(model, criterion, valid_loader):
    print("Start Validation...")
    model.eval()
    with torch.no_grad():
        cls_f1_scores, rcp_f1_scores = [], []
        cls_precision_scores, rcp_precision_scores = [], []
        cls_thr, rcp_thr = 0.5, 0.5

        for images, labels in tqdm(valid_loader, total=len(valid_loader)):
            images, labels = (
                torch.tensor(images).cuda(),
                torch.tensor(labels).cuda(),
            )
            outputs = model(images)

            cls_output, rcp_output = outputs[:, :93], outputs[:, 93:]
            food_names, ingredients = labels[:, :93], labels[:, 93:]

            cls_output = F.sigmoid(cls_output)
            rcp_output = F.sigmoid(rcp_output)
            cls_output = (cls_output >= cls_thr).float()
            rcp_output = (rcp_output >= rcp_thr).float()
            cls_f1 = f1_score(
                y_pred=cls_output.cpu(),
                y_true=food_names.cpu(),
                average="macro",
                zero_division=0,
            )
            rcp_f1 = f1_score(
                y_pred=rcp_output.cpu(),
                y_true=ingredients.cpu(),
                average="macro",
                zero_division=0,
            )
            cls_precision = precision_score(
                y_pred=cls_output.cpu(),
                y_true=food_names.cpu(),
                average="macro",
                zero_division=0,
            )
            rcp_precision = precision_score(
                y_pred=rcp_output.cpu(),
                y_true=ingredients.cpu(),
                average="macro",
                zero_division=0,
            )
            cls_f1_scores.append(cls_f1)
            rcp_f1_scores.append(rcp_f1)
            cls_precision_scores.append(cls_precision)
            rcp_precision_scores.append(rcp_precision)
        mean_cls_f1_score = sum(cls_f1_scores) / len(cls_f1_scores)
        mean_rcp_f1_score = sum(rcp_f1_scores) / len(rcp_f1_scores)
        mean_cls_precision_scores = sum(cls_precision_scores) / len(
            cls_precision_scores
        )
        mean_rcp_precision_scores = sum(rcp_precision_scores) / len(
            rcp_precision_scores
        )
        return [
            mean_cls_f1_score,
            mean_rcp_f1_score,
            mean_cls_precision_scores,
            mean_rcp_precision_scores,
        ]


def combine_train(
    model, optimizer, criterion, scheduler, train_loader, valid_loader, args
):
    print("Start Train...")

    scaler = torch.cuda.amp.GradScaler(enabled=True)
    best_cls_f1_score, best_rcp_f1_score = 0, 0
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
                loss = criterion(outputs, labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            current_lr = optimizer.param_groups[0]["lr"]
            wandb.log(
                {
                    "train/LR": current_lr,
                    "train/loss": loss,
                }
            )

        print(
            f"Duration :{datetime.datetime.now() - cur_time} |"
            f"Epoch [{epoch+1}/{args.epochs}], "
            f"Loss: {round(loss.item(),4)}, "
        )

        wandb.log({"train/Epoch": epoch + 1})
        scheduler.step()

        score = combine_validation(model, criterion, valid_loader)

        print(
            f"Validation CLS Marco F1 Score : {score[0]}\tValidation RCP Marco F1 Score : {score[1]}\n"
            f"Validation CLS Marco Precision Score : {score[2]}\tValidation RCP Marco Precision Score : {score[3]}\n"
        )
        wandb.log(
            {
                "val/cls_F1-Score": score[0],
                "val/rcp_F1-Score": score[1],
                "val/cls_Precision-Score": score[2],
                "val/rcp_Precision-Score": score[3],
            }
        )

        if score[0] > best_cls_f1_score and score[1] > best_rcp_f1_score:
            best_cls_f1_score = score[0]
            best_rcp_f1_score = score[1]
            output_path = os.path.join(args.save_path, f"{args.model_name}_best.pth")
            torch.save(model, output_path)
        output_path = os.path.join(args.save_path, f"{args.model_name}_latest.pth")
        torch.save(model, output_path)
    print("Finish Train!!!")
