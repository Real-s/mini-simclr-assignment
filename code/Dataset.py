from torch.utils.data import Dataset
import os
from PIL import Image
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


train_dataset = datasets.CIFAR10(
    root="../data",
    train=True,
    download=True,
    transform=transforms.ToTensor(),
)

test_loader = DataLoader( dataset=train_dataset,batch_size=4,shuffle=True,num_workers=0,drop_last=False)

img , target = train_dataset[0]

print(img.shape)
print(target)

plt.imshow(img.permute(1, 2, 0))
plt.title(str(target))
plt.axis("off")
plt.show()

#数据读取
class CIFAR10DataSet(Dataset):

    def __init__(self,root_dir):
        self.root_dir = root_dir


