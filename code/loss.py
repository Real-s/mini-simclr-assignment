import torch
from torch import nn
import torch.nn.functional as F


class NTXentLoss(nn.Module):
    def __init__(self, temperature=0.5):
        super().__init__()
        self.temperature = temperature

    def forward(self, z1, z2):
        batch_size = z1.shape[0]

        # [N, D] + [N, D] -> [2N, D]
        z = torch.cat([z1, z2], dim=0)

        # L2 normalize
        z = F.normalize(z, dim=1)

        # cosine similarity matrix: [2N, 2N]
        similarity = torch.matmul(z, z.T)

        # temperature scaling
        logits = similarity / self.temperature

        # mask self-similarity
        mask = torch.eye(
            2 * batch_size,
            dtype=torch.bool,
            device=z.device
        )
        logits = logits.masked_fill(mask, -1e9)

        # positive pair labels
        labels = torch.cat([
            torch.arange(batch_size, 2 * batch_size),
            torch.arange(0, batch_size)
        ]).to(z.device)

        loss = F.cross_entropy(logits, labels)
        return loss


if __name__ == "__main__":
    loss_fn = NTXentLoss(temperature=0.5)

    z1 = torch.randn(4, 128)
    z2 = torch.randn(4, 128)

    loss = loss_fn(z1, z2)

    print("z1 shape:", z1.shape)
    print("z2 shape:", z2.shape)
    print("loss:", loss)
    print("loss shape:", loss.shape)