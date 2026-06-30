import torch

from Dataset import get_simclr_train_loader
from model import MiniSimCLR
from loss import NTXentLoss


def train_one_epoch(model, dataloader, loss_fn, optimizer, device):
    """
    训练一个 epoch。
    """
    model.train()

    total_loss = 0.0
    num_batches = 0

    for (view1, view2), _ in dataloader:
        view1 = view1.to(device)
        view2 = view2.to(device)

        _, z1 = model(view1)
        _, z2 = model(view2)

        loss = loss_fn(z1, z2)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

    return total_loss / num_batches


def save_checkpoint(model, checkpoint_path):
    """
    保存 encoder 参数，供第五天 linear probe 使用。
    """
    torch.save(model.encoder.state_dict(), checkpoint_path)


def write_log(log_path, text):
    """
    把训练过程写入日志文件。
    """
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def main():
    """
    第四天预训练主流程。
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("当前设备：",device)

    epochs = 100
    batch_size = 64
    n_samples = 5000
    lr = 1e-3

    dataloader = get_simclr_train_loader(
        n_samples=n_samples,
        batch_size=batch_size,
    )

    model = MiniSimCLR().to(device)
    loss_fn = NTXentLoss(temperature=0.5)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(1, epochs + 1):
        avg_loss = train_one_epoch(
            model=model,
            dataloader=dataloader,
            loss_fn=loss_fn,
            optimizer=optimizer,
            device=device,
        )

        log_text = f"epoch {epoch}/{epochs}, contrastive loss: {avg_loss:.4f}"
        print(log_text)
        write_log("../logs/pretrain.log", log_text)

    save_checkpoint(model, "../checkpoints/simclr_encoder.pth")


if __name__ == "__main__":
    main()