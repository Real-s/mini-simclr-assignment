import json
import torch
from torch import nn

from Dataset import get_linear_probe_train_loader, get_test_loader
from model import CNNModel


def train_one_epoch(encoder, classifier, train_loader, criterion, optimizer, device):
    encoder.eval()
    classifier.train()

    total_loss = 0.0
    num_batches = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        # encoder 冻结，只负责提取特征
        with torch.no_grad():
            features = encoder(images)

        logits = classifier(features)
        loss = criterion(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

    return total_loss / num_batches


def evaluate(encoder, classifier, test_loader, device):
    encoder.eval()
    classifier.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            features = encoder(images)
            logits = classifier(features)

            preds = logits.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    accuracy = correct / total
    return accuracy


def save_results(result_path, results):
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("当前设备：", device)

    train_samples = 1000
    test_samples = 1000
    batch_size = 32
    pretrain_epochs = 3
    linear_probe_epochs = 3
    lr = 1e-3

    train_loader = get_linear_probe_train_loader(
        n_samples=train_samples,
        batch_size=batch_size,
    )

    test_loader = get_test_loader(
        n_samples=test_samples,
        batch_size=batch_size,
    )

    encoder = CNNModel(feature_dim=128).to(device)

    checkpoint_path = "../checkpoints/simclr_encoder.pth"
    encoder.load_state_dict(
        torch.load(checkpoint_path, map_location=device, weights_only=True)
    )

    for param in encoder.parameters():
        param.requires_grad = False

    classifier = nn.Linear(128, 10).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(classifier.parameters(), lr=lr)

    for epoch in range(1, linear_probe_epochs + 1):
        avg_loss = train_one_epoch(
            encoder=encoder,
            classifier=classifier,
            train_loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )

        accuracy = evaluate(
            encoder=encoder,
            classifier=classifier,
            test_loader=test_loader,
            device=device,
        )

        print(
            f"epoch {epoch}/{linear_probe_epochs}, "
            f"linear probe loss: {avg_loss:.4f}, "
            f"test accuracy: {accuracy:.4f}"
        )

    results = {
        "train_samples": train_samples,
        "test_samples": test_samples,
        "pretrain_epochs": pretrain_epochs,
        "linear_probe_epochs": linear_probe_epochs,
        "batch_size": batch_size,
        "learning_rate": lr,
        "test_accuracy": accuracy,
    }

    save_results("../results/linear_probe_results.json", results)


if __name__ == "__main__":
    main()