from torch import nn
import torch


class CNNModel(nn.Module):
    """
    feature_dim 特征层数
    """

    def __init__(self , feature_dim):
        super().__init__()

        self.CNN_Net = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),   # 32x32 -> 16x16

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),   # 16x16 -> 8x8

            nn.Conv2d(64, feature_dim, kernel_size=3, padding=1),
            nn.ReLU(),

            nn.AdaptiveAvgPool2d((1, 1)),  # [B, feature_dim, 1, 1]
            nn.Flatten(),                  # [B, feature_dim]
        )

    def forward(self , x):
        return self.CNN_Net(x)


class ProjectionHead(nn.Module):
    def __init__(self, input_dim=128, hidden_dim=512, output_dim=128):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)

class MiniSimCLR(nn.Module):
    def __init__(self, feature_dim=128, projection_dim=128):
        super().__init__()

        self.encoder = CNNModel(feature_dim=feature_dim)
        self.projection_head = ProjectionHead(
            input_dim=feature_dim,
            hidden_dim=512,
            output_dim=projection_dim,
        )

    def forward(self, x):
        features = self.encoder(x)
        projections = self.projection_head(features)
        return features, projections

if __name__ == "__main__":
    model = MiniSimCLR()

    x = torch.randn(4, 3, 32, 32)
    features, projections = model(x)

    print("input shape:", x.shape)
    print("features shape:", features.shape)
    print("projections shape:", projections.shape)


