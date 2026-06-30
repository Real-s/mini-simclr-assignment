from pathlib import Path
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_ROOT = PROJECT_ROOT / "data"


class TwoCropTransform:
    def __init__(self, transform):
        self.transform = transform

    def __call__(self, data):
        view1 = self.transform(data)
        view2 = self.transform(data)
        return view1, view2


def get_simclr_transform():
    return transforms.Compose([
        transforms.RandomResizedCrop(size=32, scale=(0.2, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(
            brightness=0.4,
            contrast=0.4,
            saturation=0.4,
            hue=0.1,
        ),
        transforms.RandomGrayscale(p=0.2),
        transforms.ToTensor(),
    ])


def get_eval_transform():
    return transforms.Compose([
        transforms.ToTensor(),
    ])


def get_simclr_train_dataset(root=DEFAULT_DATA_ROOT, n_samples=1000):
    base_transform = get_simclr_transform()
    train_dataset = datasets.CIFAR10(
        root=str(root),
        train=True,
        download=True,
        transform=TwoCropTransform(base_transform),
    )

    if n_samples is not None:
        train_dataset = Subset(train_dataset, range(n_samples))

    return train_dataset


def get_linear_probe_train_dataset(root=DEFAULT_DATA_ROOT, n_samples=1000):
    train_dataset = datasets.CIFAR10(
        root=str(root),
        train=True,
        download=True,
        transform=get_eval_transform(),
    )

    if n_samples is not None:
        train_dataset = Subset(train_dataset, range(n_samples))

    return train_dataset


def get_test_dataset(root=DEFAULT_DATA_ROOT, n_samples=1000):
    test_dataset = datasets.CIFAR10(
        root=str(root),
        train=False,
        download=True,
        transform=get_eval_transform(),
    )

    if n_samples is not None:
        test_dataset = Subset(test_dataset, range(n_samples))

    return test_dataset


def get_simclr_train_loader(root=DEFAULT_DATA_ROOT, n_samples=1000, batch_size=32):
    dataset = get_simclr_train_dataset(root=root, n_samples=n_samples)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0, drop_last=True)


def get_linear_probe_train_loader(root=DEFAULT_DATA_ROOT, n_samples=1000, batch_size=32):
    dataset = get_linear_probe_train_dataset(root=root, n_samples=n_samples)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)


def get_test_loader(root=DEFAULT_DATA_ROOT, n_samples=1000, batch_size=32):
    dataset = get_test_dataset(root=root, n_samples=n_samples)
    return DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)


if __name__ == "__main__":
    ds = get_simclr_train_dataset(n_samples=8)
    (view1, view2), label = ds[0]
    print(view1.shape, view2.shape, label)

    ds2 = get_test_dataset(n_samples=8)
    img, test_label = ds2[0]
    print(img.shape, test_label)

    loader = get_simclr_train_loader(n_samples=8, batch_size=4)
    (batch_view1, batch_view2), batch_labels = next(iter(loader))
    print(batch_view1.shape, batch_view2.shape, batch_labels.shape)
