import re
from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch import nn

from Dataset import get_test_dataset
from model import CNNModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "logs" / "pretrain.log"
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
FIGURE_DIR = PROJECT_ROOT / "report" / "figures"
DATA_ROOT = PROJECT_ROOT / "data"

CIFAR10_CLASSES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def read_latest_pretrain_losses(log_path):
    pattern = re.compile(r"epoch\s+(\d+)/(\d+),\s+contrastive loss:\s+([0-9.]+)")
    records = []

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                epoch = int(match.group(1))
                total_epochs = int(match.group(2))
                loss = float(match.group(3))
                records.append((epoch, total_epochs, loss))

    if not records:
        raise ValueError(f"No contrastive loss records found in {log_path}")

    latest_total_epochs = records[-1][1]
    return records[-latest_total_epochs:]


def save_loss_curve(loss_records, output_path):
    epochs = [record[0] for record in loss_records]
    losses = [record[2] for record in loss_records]

    plt.figure(figsize=(6, 4))
    plt.plot(epochs, losses, marker="o")
    plt.xlabel("Epoch")
    plt.ylabel("Contrastive Loss")
    plt.title("SimCLR Pretraining Loss")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def load_linear_probe_model(device):
    encoder = CNNModel(feature_dim=128).to(device)
    classifier = nn.Linear(128, 10).to(device)

    encoder.load_state_dict(
        torch.load(
            CHECKPOINT_DIR / "simclr_encoder.pth",
            map_location=device,
            weights_only=True,
        )
    )
    classifier.load_state_dict(
        torch.load(
            CHECKPOINT_DIR / "linear_classifier.pth",
            map_location=device,
            weights_only=True,
        )
    )

    encoder.eval()
    classifier.eval()
    return encoder, classifier


def save_prediction_examples(encoder, classifier, output_path, device, num_examples=5):
    dataset = get_test_dataset(root=DATA_ROOT, n_samples=1000)

    fig, axes = plt.subplots(1, num_examples, figsize=(3 * num_examples, 3.5))
    if num_examples == 1:
        axes = [axes]

    with torch.no_grad():
        for index, ax in enumerate(axes):
            image, label = dataset[index]
            logits = classifier(encoder(image.unsqueeze(0).to(device)))
            pred = logits.argmax(dim=1).item()

            image_for_plot = image.permute(1, 2, 0).cpu().numpy()
            status = "correct" if pred == label else "wrong"

            ax.imshow(image_for_plot)
            ax.set_title(
                f"true: {CIFAR10_CLASSES[label]}\n"
                f"pred: {CIFAR10_CLASSES[pred]}\n"
                f"{status}",
                fontsize=9,
            )
            ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def main():
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    loss_records = read_latest_pretrain_losses(LOG_PATH)
    save_loss_curve(loss_records, FIGURE_DIR / "loss_curve.png")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    encoder, classifier = load_linear_probe_model(device)
    save_prediction_examples(
        encoder=encoder,
        classifier=classifier,
        output_path=FIGURE_DIR / "prediction_examples.png",
        device=device,
        num_examples=5,
    )

    print("saved:", FIGURE_DIR / "loss_curve.png")
    print("saved:", FIGURE_DIR / "prediction_examples.png")


if __name__ == "__main__":
    main()

