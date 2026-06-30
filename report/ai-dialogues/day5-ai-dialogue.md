# 第 5 天：Linear Probe

- Entire session id: `019f1776-d7e6-7602-b65b-d0837327d61a`
- 来源：`.entire/metadata/019f1776-d7e6-7602-b65b-d0837327d61a/full.jsonl`

## 用户 - 2026-06-30T07:38:38.612Z

第五天 根据weekly-plan和我的文件进度 告诉我接下来该做些什么

---

## AI - 2026-06-30T07:38:45.388Z

我先按你的项目规则走：只做读取和分析，不改文件。会先快速看一下记忆里关于这个仓库的约定，再对照 `weekly-plan` 和当前文件状态给你第五天的下一步清单。

---

## AI - 2026-06-30T07:39:06.358Z

我已经确认这个仓库的既定偏好是“学习阶段，以建议为主，不直接替你改代码”。接下来我会看计划文件、代码/日志/结果目录和 git 状态，判断你现在卡在第五天的哪一段。

---

## AI - 2026-06-30T07:39:25.890Z

从目录状态看，你第 1 到第 4 天的主体文件已经存在，`checkpoints/simclr_encoder.pth` 也已经生成；第五天的关键缺口是还没有 `linear_probe.py` 和结果文件。现在我再看一下模型/预训练保存方式，避免给你一个和现有代码接口对不上的建议。

---

## AI - 2026-06-30T07:39:43.756Z

这里有个好消息：你的提交粒度已经很像计划要求，最近一次提交正好停在第 4 天预训练。第五天你要做的是在现有 checkpoint 上接一个“只训练线性层”的评估脚本，而不是再动 SimCLR 预训练主体。

---

## AI - 2026-06-30T07:39:58.654Z

还有一个小细节：`git status --ignored` 显示 checkpoint、weekly-plan、AGENTS 等被 ignore 了，`logs/pretrain.log` 目前是未跟踪文件。第五天结束前你要特别确认哪些产物老师要求提交、哪些只是本地运行产物，别到最后发现报告引用的结果文件没进仓库。

---

## AI - 2026-06-30T07:40:27.774Z

你现在的进度已经到 **第 5 天起点**：前四天主体完成了。

证据是：

- 已有 [code/Dataset.py](D:/Desktop/MedAI/mini-simclr-assignment/code/Dataset.py)、[code/model.py](D:/Desktop/MedAI/mini-simclr-assignment/code/model.py)、[code/loss.py](D:/Desktop/MedAI/mini-simclr-assignment/code/loss.py)、[code/pretrain.py](D:/Desktop/MedAI/mini-simclr-assignment/code/pretrain.py)
- 已生成 [checkpoints/simclr_encoder.pth](D:/Desktop/MedAI/mini-simclr-assignment/checkpoints/simclr_encoder.pth)
- [logs/pretrain.log](D:/Desktop/MedAI/mini-simclr-assignment/logs/pretrain.log) 里最后一轮 loss 从 `3.9731 -> 3.7774 -> 3.7592`，说明预训练跑通了
- git 最新提交是 `feat: add SimCLR pretraining loop`，正好对应第 4 天
- 目前缺少第 5 天产物：`code/linear_probe.py` 和 `results/linear_probe_results.json`

**今天接下来做什么**

1. 新建 `code/linear_probe.py`

它应该做这几件事：

- 从 `model.py` 导入 `CNNModel` 或 `MiniSimCLR`
- 创建 encoder，加载 `../checkpoints/simclr_encoder.pth`
- 只保留 encoder，不用 projection head
- 冻结 encoder 参数：`requires_grad = False`
- 在 encoder 后面接一个 `nn.Linear(128, 10)` 分类器

2. 使用你已经写好的数据接口

你的 [code/Dataset.py](D:/Desktop/MedAI/mini-simclr-assignment/code/Dataset.py) 已经准备好了：

- `get_linear_probe_train_loader(...)`
- `get_test_loader(...)`

所以第五天不需要重写数据集，只需要调用它们。

建议参数先用：

```text
train samples: 1000
test samples: 1000
batch size: 32
linear probe epochs: 3
lr: 1e-3
optimizer: Adam
loss: CrossEntropyLoss
```

3. 训练时确认只更新 classifier

训练循环里应该是：

```text
images -> frozen encoder -> features -> linear classifier -> logits
logits + labels -> cross entropy
只 optimizer classifier.parameters()
```

你可以在代码里检查一下：

```text
encoder 参数 requires_grad=False
classifier 参数 requires_grad=True
```

4. 测试集上算 accuracy

每个 epoch 结束后，或者训练结束后，在 test loader 上：

```text
pred = logits.argmax(dim=1)
correct += pred == labels
accuracy = correct / total
```

最低目标不是高准确率，而是能报告：

```text
使用训练图像数：1000
测试图像数：1000
预训练 epoch：3
linear probe epoch：3
batch size：32
test accuracy：xx.xx%
```

5. 保存结果文件

把结果写到：

```text
results/linear_probe_results.json
```

建议内容包括：

```json
{
  "pretrain_epochs": 3,
  "linear_probe_epochs": 3,
  "train_samples": 1000,
  "test_samples": 1000,
  "batch_size": 32,
  "accuracy": 0.0
}
```

6. 用 MedAI 环境运行验证

写完后用项目要求的 conda 环境跑：

```powershell
conda run -n MedAI python code\linear_probe.py
```

如果你的脚本里路径用的是 `../checkpoints/...`，那就从 `code` 目录运行：

```powershell
cd code
conda run -n MedAI python linear_probe.py
```

7. 第五天结束前整理 git

现在 `logs/pretrain.log` 是未跟踪文件，`code/__pycache__/` 也未跟踪。你应该：

- 不提交 `__pycache__/`
- 考虑把 `__pycache__/` 和 `*.pyc` 加回 `.gitignore`
- 提交 `code/linear_probe.py`
- 提交 `results/linear_probe_results.json`
- 如果老师要求日志，也提交 `logs/pretrain.log`

第五天推荐 commit：

```text
feat: add linear probe evaluation
```

你现在最该做的是：**先写 `linear_probe.py`，只跑 1 个 epoch smoke test，确认 checkpoint 能加载、accuracy 能打印，再改成 3 epoch 保存 json。**

<oai-mem-citation>
<citation_entries>
MEMORY.md:59-91|note=[repo learning mode and Mini-SimCLR deliverables]
</citation_entries>
<rollout_ids>
019f0776-7e9f-7c11-b251-548f8ae5aa08
</rollout_ids>
</oai-mem-citation>

---

## 用户 - 2026-06-30T07:41:04.302Z

我需要用到什么函数 以及什么思路

---

## AI - 2026-06-30T07:41:24.201Z

你第 5 天写 `linear_probe.py`，核心就是 **“用预训练好的 encoder 提特征，只训练一个线性分类器”**。

你会用到这些函数/类：

**从你已有文件导入**

```python
from Dataset import get_linear_probe_train_loader, get_test_loader
from model import CNNModel
```

或者也可以：

```python
from model import MiniSimCLR
```

但第五天更推荐直接用 `CNNModel`，因为你已经只保存了 encoder 参数。

**PyTorch 里会用到**

```python
import torch
from torch import nn
```

主要对象：

```python
torch.load(...)
encoder.load_state_dict(...)
encoder.eval()
nn.Linear(128, 10)
nn.CrossEntropyLoss()
torch.optim.Adam(...)
torch.no_grad()
logits.argmax(dim=1)
```

**整体思路**

1. **准备设备**

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

2. **加载数据**

训练 linear probe 用有标签训练集：

```python
train_loader = get_linear_probe_train_loader(n_samples=1000, batch_size=32)
```

测试 accuracy 用测试集：

```python
test_loader = get_test_loader(n_samples=1000, batch_size=32)
```

3. **加载预训练 encoder**

你的 `pretrain.py` 保存的是：

```python
torch.save(model.encoder.state_dict(), "../checkpoints/simclr_encoder.pth")
```

所以第五天应该这样加载：

```python
encoder = CNNModel(feature_dim=128).to(device)
encoder.load_state_dict(torch.load("../checkpoints/simclr_encoder.pth", map_location=device))
```

4. **冻结 encoder**

这是 linear probe 的关键：

```python
for param in encoder.parameters():
    param.requires_grad = False
```

意思是：encoder 不再学习，只当作“特征提取器”。

5. **添加线性分类器**

CIFAR-10 有 10 类，你的 encoder 输出是 128 维，所以：

```python
classifier = nn.Linear(128, 10).to(device)
```

6. **只优化 classifier**

```python
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(classifier.parameters(), lr=1e-3)
```

注意这里不要写 `encoder.parameters()`，否则就不是冻结评估了。

7. **训练 linear probe**

每个 batch 的流程是：

```text
image -> encoder -> feature -> classifier -> logits -> cross entropy loss
```

代码结构大概是：

```python
encoder.eval()
classifier.train()

for images, labels in train_loader:
    images = images.to(device)
    labels = labels.to(device)

    with torch.no_grad():
        features = encoder(images)

    logits = classifier(features)
    loss = criterion(logits, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

8. **测试 accuracy**

测试时 encoder 和 classifier 都用 eval：

```python
encoder.eval()
classifier.eval()
```

然后统计：

```python
preds = logits.argmax(dim=1)
correct += (preds == labels).sum().item()
total += labels.size(0)
accuracy = correct / total
```

9. **保存结果**

最后把这些信息保存到 `results/linear_probe_results.json`：

```text
train_samples
test_samples
pretrain_epochs
linear_probe_epochs
batch_size
accuracy
```

你可以把 `linear_probe.py` 拆成 4 个函数，结构会比较清楚：

```python
def train_one_epoch(encoder, classifier, train_loader, criterion, optimizer, device):
    ...

def evaluate(encoder, classifier, test_loader, device):
    ...

def save_results(result_path, results):
    ...

def main():
    ...
```

最重要的理解是：

```text
pretrain 阶段：encoder + projection head 一起学“图像表征”
linear probe 阶段：扔掉 projection head，冻结 encoder，只训练一个 Linear 分类头
```

如果 linear probe accuracy 不高也没关系，第 5 天的目标是证明：**你预训练得到的 encoder 可以被加载、冻结，并用于 CIFAR-10 分类评估。**

---

## 用户 - 2026-06-30T07:44:44.383Z

给出总体示例

---

## AI - 2026-06-30T07:45:03.898Z

下面是 **总体示例结构**。你可以照着写，但建议你自己手打一遍、边写边理解每一步。

```python
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
        torch.load(checkpoint_path, map_location=device)
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
```

运行方式建议在 `code` 目录下运行：

```powershell
cd code
conda run -n MedAI python linear_probe.py
```

这个示例的主线就是：

```text
加载 CIFAR-10 有标签数据
加载预训练 encoder
冻结 encoder
新建 Linear(128, 10)
只训练 Linear 分类器
在 test split 上算 accuracy
保存 json 结果
```

你写完之后，先把 `linear_probe_epochs = 1` 跑通；确认没报错、能打印 accuracy，再改回 `3`。

---

## 用户 - 2026-06-30T07:47:26.094Z

D:\Desktop\MedAI\mini-simclr-assignment\code\linear_probe.py:90: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  torch.load(checkpoint_path, map_location=device)

---

## AI - 2026-06-30T07:47:37.744Z

这个不是报错，是 **FutureWarning**：程序还能正常跑。意思是 PyTorch 提醒你：以后 `torch.load()` 默认会更安全，现在建议你显式写 `weights_only=True`。

你这里加载的是自己训练保存的：

```python
torch.save(model.encoder.state_dict(), "../checkpoints/simclr_encoder.pth")
```

也就是纯参数字典，所以可以把 `linear_probe.py` 第 90 行改成：

```python
encoder.load_state_dict(
    torch.load(checkpoint_path, map_location=device, weights_only=True)
)
```

完整位置大概是：

```python
checkpoint_path = "../checkpoints/simclr_encoder.pth"

state_dict = torch.load(
    checkpoint_path,
    map_location=device,
    weights_only=True,
)

encoder.load_state_dict(state_dict)
```

这样 warning 就会消失。

如果你改完后出现：

```text
TypeError: 'weights_only' is an invalid keyword argument
```

说明你的 PyTorch 版本偏旧，那就先保留原写法也可以：

```python
encoder.load_state_dict(
    torch.load(checkpoint_path, map_location=device)
)
```

你的情况里，推荐先试 `weights_only=True`。这不会影响 linear probe 的逻辑，只是让 checkpoint 加载方式更安全、更符合新版 PyTorch 的要求。

---

## 用户 - 2026-06-30T07:49:21.203Z

当前设备： cuda
Files already downloaded and verified
Files already downloaded and verified
epoch 1/3, linear probe loss: 2.2829, test accuracy: 0.1760
epoch 2/3, linear probe loss: 2.2463, test accuracy: 0.1860
epoch 3/3, linear probe loss: 2.2183, test accuracy: 0.2300

---

## AI - 2026-06-30T07:49:35.662Z

这个结果是 **正常且可用的**，第 5 天已经跑通了。

你现在可以记录成：

```text
当前设备：cuda
linear probe epochs：3
test samples：1000
final test accuracy：0.2300 / 23.00%
```

从数值上看也合理：

```text
epoch 1: loss 2.2829, accuracy 17.60%
epoch 2: loss 2.2463, accuracy 18.60%
epoch 3: loss 2.2183, accuracy 23.00%
```

CIFAR-10 随机猜测大约是 10%，你现在到 23%，说明 encoder 提取到了一些有用特征。loss 也在下降，accuracy 也在升，这比“只是能跑通”更好一点。

接下来做三件事：

1. 确认生成了结果文件

看一下是否有：

```text
results/linear_probe_results.json
```

里面应该包含最终 `test_accuracy: 0.23`。

2. 把这段结果写进报告草稿

可以这样写：

```text
Linear probe 阶段冻结预训练 encoder，仅训练一个线性分类器。
使用 1000 张 CIFAR-10 训练图像训练 linear probe，并在 1000 张测试图像上评估。
训练 3 个 epoch 后，测试准确率从 17.60% 提升到 23.00%，最终 accuracy 为 23.00%。
该结果高于随机猜测的 10%，说明预训练 encoder 学到了一定的图像表征能力。
```

3. 准备提交第 5 天 commit

建议提交：

```text
code/linear_probe.py
results/linear_probe_results.json
```

commit message：

```text
feat: add linear probe evaluation
```

如果你还没有处理 `__pycache__`，不要提交它。最好把 `.gitignore` 里这两行取消注释：

```text
__pycache__/
*.pyc
```

今天的核心目标已经完成。下一步就是第 6 天：画 loss 曲线和保存至少 5 张预测图片。

---

