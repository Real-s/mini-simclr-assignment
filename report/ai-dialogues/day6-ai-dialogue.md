# 第 6 天：结果整理与可视化

- Entire session id: `019f17ad-2eb3-77c2-8132-b897178be715`
- 来源：`.entire/metadata/019f17ad-2eb3-77c2-8132-b897178be715/full.jsonl`

## 用户 - 2026-06-30T08:37:50.430Z

第六天 根据weekly-plan和我的文件进度 告诉我接下来该做些什么

---

## AI - 2026-06-30T08:37:56.651Z

我先按你的学习模式来做只读梳理：看一下周计划、当前仓库文件和已有进度，再把第六天该做的事整理成可执行清单。

---

## AI - 2026-06-30T08:38:14.518Z

我已经确认这个仓库有明确的“偏指导、不直接改代码”偏好。接下来我会重点看 `weekly-plan.md`、README 要求，以及 `code/report/results/logs/checkpoints` 里哪些东西已经完成。

---

## AI - 2026-06-30T08:38:28.125Z

从文件进度看，前 4 天的主体代码基本在位：`Dataset.py/model.py/loss.py/pretrain.py` 和 `checkpoints/simclr_encoder.pth` 已经有了。但第 5 天的 `linear_probe.py`、结果 JSON、训练日志、报告图片目前还没出现，所以第六天不能直接跳到画图，得先补齐评估证据。

---

## AI - 2026-06-30T08:38:45.900Z

还有一个小细节：`git log` 里有一条 “add linear probe evaluation”，但工作区文件列表里没有看到 `code/linear_probe.py`，`results/` 也还是空壳。这说明下一步要先核对第 5 天到底是“提交名写了”还是“代码后来不在当前版本里”。

---

## AI - 2026-06-30T08:39:04.710Z

现在更清楚了：第 5 天的代码曾经在历史提交 `8f8db39` 里出现过，包含 `code/linear_probe.py`、`logs/pretrain.log` 和 `results/linear_probe_results.json`；但当前 HEAD 里这些文件已经没有了。第六天开始前，最好先把这个“历史里有、当前没有”的断点弄清楚，否则报告证据会断。

---

## AI - 2026-06-30T08:39:15.913Z

我还看了后续提交：`3ab9bbc` 明确删除了第 5 天那三个关键文件，提交名是修 Entire 对话。也就是说今天的首要任务不是“继续写新功能”，而是先恢复或重做 linear probe 证据，然后再做第六天的图表整理。

---

## AI - 2026-06-30T08:39:43.734Z

根据我刚才只读检查，你第六天不要直接画图，应该先补上“第 5 天评估证据”，再做结果整理。

当前进度判断：

- 已有：`Dataset.py`、`model.py`、`loss.py`、`pretrain.py`
- 已有 checkpoint：`checkpoints/simclr_encoder.pth`
- 缺失：`code/linear_probe.py`
- 缺失：`logs/pretrain.log`
- 缺失：`results/linear_probe_results.json`
- 缺失：`report/figures/loss_curve.png`
- 缺失：`report/figures/prediction_examples.png`
- 关键发现：`linear_probe.py` 曾经在提交 `8f8db39 feat: add linear probe evaluation` 里存在，但后来被 `3ab9bbc fix: 修复entire对话` 删除了。

所以接下来建议按这个顺序做：

1. 先恢复或重写第 5 天的 linear probe  
   你可以先查看历史版本：

   ```powershell
   git show 8f8db39:code/linear_probe.py
   ```

   如果确认那就是你要的版本，再考虑恢复：

   ```powershell
   git restore --source=8f8db39 -- code/linear_probe.py logs/pretrain.log results/linear_probe_results.json
   ```

2. 用 `MedAI` 环境重新验证 linear probe  
   确认它能加载 `checkpoints/simclr_encoder.pth`，冻结 encoder，训练 linear classifier，并输出 accuracy。

   建议记录这些信息：训练图像数、测试图像数、epoch、batch size、learning rate、accuracy。

3. 再做第六天真正的任务：结果可视化  
   需要生成：

   - `report/figures/loss_curve.png`
   - `report/figures/prediction_examples.png`

   虽然 `report-template.md` 写至少 3 个样例，但 `weekly-plan.md` 写至少 5 张测试图片，建议按 5 张做，更稳。

4. 把结果写进 `results/`  
   至少有一个 JSON 或文本文件，包含：

   ```text
   pretrain_images
   pretrain_epochs
   linear_probe_train_images
   test_images
   linear_probe_epochs
   batch_size
   temperature
   test_accuracy
   ```

5. 开始填报告，不用等第 7 天才动  
   今天可以先填这些部分：

   - 数据集
   - 数据增强
   - 模型结构
   - Loss 实现
   - 训练设置
   - 训练过程 loss 表格
   - Linear probe accuracy
   - 预测结果展示
   - 如果 accuracy 接近 10%，写原因分析

6. 今天结束前做一次小步提交  
   合适的 commit message：

   ```text
   feat: save training curves and prediction examples
   ```

   如果你先恢复了 linear probe，也可以先单独提交：

   ```text
   feat: restore linear probe evaluation
   ```

最重要的一句话：你现在的第六天任务，第一步是把被删除的第 5 天 `linear_probe` 和结果证据补回来；等 accuracy、loss 日志、预测样例都存在后，再画图和写报告分析。

<oai-mem-citation>
<citation_entries>
MEMORY.md:59-95|note=[repo learning preference and weekly Mini-SimCLR planning context]
</citation_entries>
<rollout_ids>
019f0776-7e9f-7c11-b251-548f8ae5aa08
</rollout_ids>
</oai-mem-citation>

---

## 用户 - 2026-06-30T08:42:32.118Z

现在在看一下呢

---

## AI - 2026-06-30T08:42:40.648Z

我会重新做一次只读检查：当前文件、git 状态、关键产物是否已经恢复或新增，然后对照第六天任务给你结论。

---

## AI - 2026-06-30T08:43:00.707Z

状态有明显变化：`linear_probe.py`、`logs/pretrain.log`、`results/linear_probe_results.json` 已经回来了，工作区也是干净的。现在我看一下结果内容和脚本是否足够支撑第六天。

---

## AI - 2026-06-30T08:43:12.635Z

第 5 天现在基本恢复了；第 6 天还没开始，因为 `report/figures` 里只有 `.gitkeep`。我再确认一下有没有已经写好的可视化脚本或隐藏结果文件，避免漏看。

---

## AI - 2026-06-30T08:43:26.261Z

现在状态比刚才好了，核心断点已经修复：

- `code/linear_probe.py` 已恢复
- `logs/pretrain.log` 已恢复
- `results/linear_probe_results.json` 已恢复
- `git status --short` 为空，说明当前工作区干净
- 当前最新提交是 `8f8db39 feat: add linear probe evaluation`

当前结果：

```text
train_samples: 1000
test_samples: 1000
pretrain_epochs: 3
linear_probe_epochs: 3
batch_size: 32
learning_rate: 0.001
test_accuracy: 0.23
```

也就是 linear probe accuracy 是 **23%**，高于随机猜测 10%，可以写进报告。

但第六天还没完成。现在还缺：

```text
report/figures/loss_curve.png
report/figures/prediction_examples.png
```

下一步建议：

1. 写一个可视化脚本，例如 `code/visualize_results.py`
2. 从 `logs/pretrain.log` 读取 contrastive loss，画 loss 曲线
3. 加载 encoder + linear classifier，保存 5 张测试图片预测结果
4. 输出：
   ```text
   report/figures/loss_curve.png
   report/figures/prediction_examples.png
   ```
5. 把 accuracy 23% 和 loss 下降情况写进报告

注意一个小问题：`pretrain.log` 里有多段记录：

```text
epoch 1/1 ...
epoch 1/3 ...
epoch 2/3 ...
epoch 3/3 ...
epoch 1/3 ...
epoch 2/3 ...
epoch 3/3 ...
```

报告里建议用最后一组 3 epoch：

```text
epoch 1/3, contrastive loss: 3.9731
epoch 2/3, contrastive loss: 3.7774
epoch 3/3, contrastive loss: 3.7592
```

结论：现在可以正式进入第六天，任务重点是“画图 + 保存预测样例 + 整理结果分析”。

---

## 用户 - 2026-06-30T08:43:50.604Z

告诉我接下来该做些什么

---

## AI - 2026-06-30T08:44:09.354Z

接下来按这个顺序做，不要跳步：

1. 新建第六天可视化脚本  
   建议文件名：

   ```text
   code/visualize_results.py
   ```

   它要做两件事：

   - 读取 `logs/pretrain.log`，画 contrastive loss 曲线
   - 用测试集取 5 张图片，展示真实类别、预测类别、是否正确

2. 先画 loss 曲线  
   使用最后一组 3 epoch 记录：

   ```text
   epoch 1: 3.9731
   epoch 2: 3.7774
   epoch 3: 3.7592
   ```

   输出到：

   ```text
   report/figures/loss_curve.png
   ```

3. 再做预测样例图  
   你需要：

   - 加载 `checkpoints/simclr_encoder.pth`
   - 创建同样的 `nn.Linear(128, 10)` classifier
   - 注意：你现在只保存了 encoder，没有保存 linear classifier 权重

   所以这里有一个关键问题：如果想画“真实预测结果”，你需要先修改 `linear_probe.py`，在训练结束后保存 classifier：

   ```text
   checkpoints/linear_classifier.pth
   ```

   否则预测图只能用一个随机初始化 classifier，结果没有意义。

4. 修改 `linear_probe.py` 的建议  
   在训练结束后保存：

   ```python
   torch.save(classifier.state_dict(), "../checkpoints/linear_classifier.pth")
   ```

   然后重新运行：

   ```powershell
   conda run -n MedAI python code\linear_probe.py
   ```

5. 生成预测展示图  
   `visualize_results.py` 加载：

   ```text
   checkpoints/simclr_encoder.pth
   checkpoints/linear_classifier.pth
   ```

   输出：

   ```text
   report/figures/prediction_examples.png
   ```

   图中至少 5 张测试图片，每张显示：

   ```text
   true: cat
   pred: dog
   wrong
   ```

6. 更新 `results/linear_probe_results.json`  
   建议补充这些字段：

   ```json
   {
     "train_samples": 1000,
     "test_samples": 1000,
     "pretrain_epochs": 3,
     "linear_probe_epochs": 3,
     "batch_size": 32,
     "learning_rate": 0.001,
     "test_accuracy": 0.23,
     "encoder_checkpoint": "checkpoints/simclr_encoder.pth",
     "classifier_checkpoint": "checkpoints/linear_classifier.pth",
     "loss_curve": "report/figures/loss_curve.png",
     "prediction_examples": "report/figures/prediction_examples.png"
   }
   ```

7. 报告里今天先填这些部分  
   不用等第七天：

   - 第 8 节：训练过程
   - 第 9 节：Linear Probe 结果
   - 第 10 节：预测结果展示
   - 第 11 节：问题与改进

   可以这样写核心结论：

   ```text
   contrastive loss 从 3.9731 降到 3.7592，说明预训练过程能够正常优化。
   linear probe 在 1000 张测试图像上达到 23% accuracy，高于 CIFAR-10 随机猜测的 10%，说明 encoder 学到了一定图像表征。
   但准确率仍然较低，可能原因包括预训练 epoch 较少、训练样本只有 1000 张、CNN encoder 较浅、CPU 训练时间有限。
   ```

8. 最后提交一次  
   如果你完成了 classifier 保存和可视化，提交：

   ```powershell
   git add code\linear_probe.py code\visualize_results.py checkpoints\linear_classifier.pth results\linear_probe_results.json report\figures\loss_curve.png report\figures\prediction_examples.png
   git commit -m "feat: save training curves and prediction examples"
   ```

最关键的一步是第 3 步：**先保存 linear classifier 权重**。不然 prediction examples 没有可信度。

---

## 用户 - 2026-06-30T08:45:36.766Z

我现在代码部分的任务已经完完成了是吗

---

## AI - 2026-06-30T08:45:45.906Z

不完全算完成。按当前文件状态判断：

**核心训练代码已经基本完成：**

- `code/Dataset.py`：数据加载和双视图增强已完成
- `code/model.py`：encoder + projection head 已完成
- `code/loss.py`：NT-Xent loss 已完成
- `code/pretrain.py`：自监督预训练已完成
- `code/linear_probe.py`：linear probe 已恢复并完成
- `results/linear_probe_results.json`：已有 accuracy，当前是 `0.23`

但**第六天需要的代码部分还差一点**：

- 还没有 `code/visualize_results.py`
- 还没有生成 `report/figures/loss_curve.png`
- 还没有生成 `report/figures/prediction_examples.png`
- 当前 `linear_probe.py` 只保存了结果 JSON，没有保存 `linear_classifier.pth`，所以后面预测样例图缺少可复现的分类器权重

所以结论是：

```text
前 5 天的代码任务基本完成。
第 6 天的可视化代码和预测展示还没完成。
```

你现在接下来只需要补“结果整理与可视化”这一块，不需要再大改 SimCLR 主体代码。

---

## 用户 - 2026-06-30T08:46:37.881Z

visualize_results这个文件夹里我该完成那些任务 写一些什么代码呢 你能帮我完成吗

---

## AI - 2026-06-30T08:46:48.814Z

可以。我会直接补一个 `code/visualize_results.py`，同时小改 `linear_probe.py` 保存分类器权重；这样预测样例图不是随机分类器输出，而是能复现实验结果。先检查一下当前脚本细节和路径。

---

## AI - 2026-06-30T08:47:04.783Z

我会做两处编辑：`linear_probe.py` 保存 `linear_classifier.pth` 并把路径改成基于项目根目录；新增 `visualize_results.py` 生成 loss 曲线和 5 张预测图。这样从项目根目录运行也不会因为 `../` 路径出错。

---

## AI - 2026-06-30T08:49:41.187Z

`apply_patch` 被当前 Windows 沙箱 helper 拦住了，不是代码问题。我会改用 PowerShell 在工作区内写入文件，并保持修改范围只限这两个脚本。

---

## AI - 2026-06-30T08:50:40.602Z

代码已经补上。现在需要按顺序运行：先重新跑 `linear_probe.py` 生成 `checkpoints/linear_classifier.pth`，再跑 `visualize_results.py` 生成两张图片。

---

## AI - 2026-06-30T08:51:09.222Z

运行失败不是训练逻辑问题，是 `conda run` 在 Windows GBK 输出中文时触发了 `UnicodeEncodeError`。我会把脚本里的中文 `print` 改成英文输出，再重新验证。

---

## AI - 2026-06-30T08:51:23.857Z

已把输出改成英文。现在重新跑 linear probe；如果成功，会生成分类器权重和更新结果 JSON。

---

## AI - 2026-06-30T08:51:50.541Z

现在失败点变成数据目录权限：`torchvision` 想重新解压 CIFAR-10，但 `data/cifar-10-batches-py/data_batch_4` 拒绝写入。先不删除数据；我会检查这个目录权限和现有文件状态，再决定是复用已有数据还是换一个临时数据目录。

---

## AI - 2026-06-30T08:52:04.392Z

`data/cifar-10-batches-py` 当前连读取 ACL 都被拒绝，说明这个目录本身权限坏了。为避免删除或改权限，我会让第六天脚本使用新的本地数据目录 `data_working/`，并把它加入 `.gitignore`。这样不碰坏掉的原目录。

---

## AI - 2026-06-30T08:52:35.956Z

发现 PowerShell 替换时把换行写成了字面量 `` `n``，我现在修正格式；这是文件写入方式的问题，不是业务逻辑。

---

## AI - 2026-06-30T08:53:11.361Z

`visualize_results.py` 已经使用 `data_working`，但 `linear_probe.py` 的 dataloader 参数还没带上 `root=DATA_ROOT`。我补上这一点。

---

## AI - 2026-06-30T08:53:20.571Z

现在重新运行。由于会在 `data_working/` 解压 CIFAR-10，并重新训练 3 epoch linear probe，耗时可能比刚才长一点。

---

## AI - 2026-06-30T08:53:38.511Z

`linear_probe.py` 已通过，生成了分类器权重；这次 accuracy 是 `0.2100`。接下来运行可视化脚本生成两张报告图片。

---

## AI - 2026-06-30T08:54:06.672Z

可视化脚本也通过了。最后我检查产物、结果 JSON 和图片是否确实存在。

---

## AI - 2026-06-30T08:54:17.662Z

产物已经存在。注意：`checkpoints/*.pth` 目前被 `.gitignore` 忽略，所以分类器权重生成了，但不会被普通 `git add` 加进去；如果最终提交要求包含 checkpoint，需要用 `git add -f` 或调整 `.gitignore`。我再快速看一下生成图片是否可读。

---

## AI - 2026-06-30T08:55:41.716Z

图片查看工具也被同一个 Windows sandbox helper 拦住了。我改用 Python 检查 PNG 尺寸和文件有效性。

---

## AI - 2026-06-30T08:56:00.411Z

验证通过，但 diff 显示 PowerShell 给几个文本文件加了 UTF-8 BOM。为避免无意义编码变化，我会把这些文件重写为无 BOM UTF-8，并顺手把结果 JSON 加上两张图路径。

---

## AI - 2026-06-30T08:56:08.741Z

我会把 `results/linear_probe_results.json` 补充图像路径，方便报告引用和最终检查。

---

## AI - 2026-06-30T08:56:22.071Z

最后做一次状态和产物核对。

---

## AI - 2026-06-30T08:56:45.504Z

已帮你完成第六天可视化部分。

我做了这些改动：

- 新增 [visualize_results.py](D:/Desktop/MedAI/mini-simclr-assignment/code/visualize_results.py)
  - 读取 `logs/pretrain.log`
  - 使用最后一组 3 epoch 的 contrastive loss
  - 生成 `report/figures/loss_curve.png`
  - 加载 encoder + linear classifier
  - 保存 5 张测试图片预测展示到 `report/figures/prediction_examples.png`

- 修改 [linear_probe.py](D:/Desktop/MedAI/mini-simclr-assignment/code/linear_probe.py)
  - 保存 `checkpoints/linear_classifier.pth`
  - 修正路径为基于项目根目录，避免从不同目录运行时报错
  - 改用 `data_working/`，避开你原来 `data/cifar-10-batches-py` 的权限问题

- 修改 `.gitignore`
  - 加入 `data_working/`，避免把临时数据目录提交上去

已验证运行通过：

```powershell
conda run -n MedAI python code\linear_probe.py
conda run -n MedAI python code\visualize_results.py
```

生成结果：

```text
report/figures/loss_curve.png
report/figures/prediction_examples.png
```

这次重新跑出的 linear probe accuracy 是：

```text
test_accuracy: 0.21
```

注意：`checkpoints/linear_classifier.pth` 已生成，但当前 `.gitignore` 会忽略 `checkpoints/*.pth`。如果最终提交需要包含 checkpoint，需要后面用 `git add -f checkpoints/linear_classifier.pth`。

---

## 用户 - 2026-06-30T08:58:37.796Z

我在那里调整epoch的数量

---

## AI - 2026-06-30T08:58:48.922Z

在两个地方调：

1. **预训练 epoch**

文件：`D:\Desktop\MedAI\mini-simclr-assignment\code\pretrain.py`

找到：

```python
epochs = 3
```

改成你想要的数量，比如：

```python
epochs = 5
```

然后重新运行：

```powershell
conda run -n MedAI python code\pretrain.py
```

这会重新生成：

```text
checkpoints/simclr_encoder.pth
logs/pretrain.log
```

2. **linear probe epoch**

文件：`D:\Desktop\MedAI\mini-simclr-assignment\code\linear_probe.py`

找到：

```python
linear_probe_epochs = 3
```

改成比如：

```python
linear_probe_epochs = 5
```

然后重新运行：

```powershell
conda run -n MedAI python code\linear_probe.py
```

这会重新生成：

```text
checkpoints/linear_classifier.pth
results/linear_probe_results.json
```

如果你改了预训练 epoch，建议按顺序重新跑：

```powershell
conda run -n MedAI python code\pretrain.py
conda run -n MedAI python code\linear_probe.py
conda run -n MedAI python code\visualize_results.py
```

注意：`results/linear_probe_results.json` 里的 `pretrain_epochs` 目前在 `linear_probe.py` 里也手写成了：

```python
pretrain_epochs = 3
```

如果你把 `pretrain.py` 的 `epochs` 改成 5，也要把这里同步改成：

```python
pretrain_epochs = 5
```

否则结果记录会不一致。

---

## 用户 - 2026-06-30T09:09:01.391Z

为什么我训练了100轮 contrastive loss: 2.9870 loss一直不减少呢

---

## AI - 2026-06-30T09:09:14.182Z

我先看一下你当前的 loss 实现、训练循环和日志形态；这种 “100 轮还卡在 2.98” 很可能不是单纯没学到，而是 loss 公式或 batch 内正样本标签构造有一个隐蔽问题。

---

## AI - 2026-06-30T09:09:31.401Z

我看到你的 `pretrain.py` 已经改成了 `epochs=100, n_samples=2000, batch_size=32`。接下来我看一下实际日志前后变化，判断是“完全不动”还是“下降到一个理论下限附近后震荡”。

---

## AI - 2026-06-30T09:09:54.660Z

不是没有训练到，恰恰相反：你的 loss 是下降了的。

我看了 `logs/pretrain.log`：

```text
epoch 1/100, contrastive loss: 4.1025
epoch 20/100, contrastive loss: 3.3041
epoch 71/100, contrastive loss: 3.0577
epoch 92/100, contrastive loss: 2.9820
epoch 100/100, contrastive loss: 2.9870
```

所以它不是“一直不减少”，而是前期明显下降，后期在 `3.0` 左右进入平台期。

关键原因是：你的 batch size 是 32，SimCLR 每个 batch 会有 `2N = 64` 个样本。对每个样本来说，除了自己以外有 63 个候选。随机猜时 cross entropy 大约是：

```text
log(63) ≈ 4.14
```

你的初始 loss `4.10` 很接近随机水平；最后降到 `2.99`，说明模型已经学到了东西。`2.99` 对应的“有效候选数”大约是：

```text
exp(2.99) ≈ 19.9
```

也就是说，它已经不是在 63 个里面瞎猜，而是把正样本相似度排得明显更靠前了。

另外，你的 `results/linear_probe_results.json` 里 test accuracy 是：

```text
test_accuracy: 0.4405
```

44.05% 对 CIFAR-10 小 CNN + 2000 张图 + 简化 SimCLR 来说已经明显高于随机 10%，这也证明 representation 不是废的。

为什么后面不继续降很多？

- 小型 CNN 表达能力有限，没有 ResNet 那么强。
- batch size 32 对 contrastive learning 偏小，负样本数量少。
- CIFAR-10 里同类图片会互相当“负样本”，loss 不容易接近 0。
- 数据增强比较强，同一张图两次增强后可能差别很大。
- 你的模型里没有 BatchNorm，SimCLR 训练通常会更难一点。
- contrastive loss 本身不一定越低越好看到 0，最终还是看 linear probe accuracy。

你现在第六天报告里可以这样写：

```text
Contrastive loss 从 4.1025 下降到约 2.9870。由于 batch size=32 时每个样本有 63 个候选，随机水平约为 log(63)=4.14，因此 loss 明显低于随机水平，说明模型学到了一定的图像表征。后期 loss 在 3.0 附近震荡，可能与小型 CNN 表达能力有限、batch size 较小、训练数据量有限以及数据增强较强有关。
```

建议下一步不是盲目再训 100 轮，而是做两个检查：

1. 画 loss 曲线，看是不是前期下降、后期平台。
2. 保存预测样例图，因为 44.05% accuracy 已经足够支撑报告分析。

<oai-mem-citation>
<citation_entries>
MEMORY.md:59-91|note=[repo learning preference and Mini-SimCLR deliverable context]
</citation_entries>
<rollout_ids>
019f0776-7e9f-7c11-b251-548f8ae5aa08
</rollout_ids>
</oai-mem-citation>

---

## 用户 - 2026-06-30T09:12:54.843Z

训练的时候 gpu负载不高

---

## AI - 2026-06-30T09:13:13.174Z

正常。你这个 Mini-SimCLR 训练 GPU 负载不高，主要不是坏事，而是任务太轻了。

你现在的设置大概是：

```text
CIFAR-10: 32x32 小图
n_samples: 2000
batch_size: 32
模型: 很小的 CNN
num_workers: 0
```

这几个条件都会让 GPU 吃不满。

主要原因：

1. 图片太小  
   CIFAR-10 只有 `32x32`，一批 32 张图的数据量很小。GPU 擅长大矩阵、大 batch、大模型，这里计算量不够。

2. 模型太小  
   你的 encoder 是几层 Conv + ReLU + Pool，不像 ResNet、ViT 那种大模型，GPU 一下就算完了，然后在等下一批数据。

3. `num_workers=0`  
   DataLoader 在主进程里读取和做增强。RandomResizedCrop、ColorJitter 这些增强在 CPU 上做，GPU 经常会等 CPU 准备数据，所以 GPU utilization 看起来不高。

4. batch size 32 偏小  
   对 GPU 来说 batch size 32 的 CIFAR-10 太轻。显存占用和计算负载都会低。

5. 你的训练瓶颈可能在 CPU 数据增强，而不是 GPU 计算  
   SimCLR 每张图要做两次随机增强，CPU 工作量比普通分类训练更高。

可以怎么判断是不是正常？

如果训练没有报错，并且日志 loss 从 `4.1025` 降到 `2.9870`，linear probe accuracy 到了 `44.05%`，那说明 GPU 低负载不影响结果，模型确实在学。

想让 GPU 负载高一点，可以尝试：

```python
batch_size = 128
```

以及把 DataLoader 改成：

```python
DataLoader(..., num_workers=2, pin_memory=True)
```

但在 Windows 上 `num_workers` 有时会带来多进程问题，所以建议先试 `num_workers=2`，不稳定就退回 `0`。

报告里可以这样写：

```text
训练过程中 GPU 利用率不高，主要原因是 CIFAR-10 图像尺寸较小、模型规模较轻、batch size 较小，并且 SimCLR 的随机数据增强主要在 CPU 端完成。因此本实验的瓶颈更多来自数据加载和增强，而不是 GPU 计算。
```

一句话：你这个项目 GPU 不高是预期现象，不是训练失败。当前更应该看 loss 曲线和 linear probe accuracy。

---

## 用户 - 2026-06-30T09:14:05.660Z

为什么 linear——probe 训练的时候 gpu负载很高

---

## AI - 2026-06-30T09:14:22.568Z

这也正常，而且和预训练阶段 GPU 低负载并不矛盾。

Linear probe 看起来只是“线性分类器”，但你的训练过程很可能仍然在做这些事：

```text
图片 -> encoder 前向计算 -> linear classifier -> loss -> backward
```

即使 encoder 冻结了，训练时通常还是要让每张图片通过 encoder 提取特征。冻结只表示不更新 encoder 参数，不代表不计算 encoder 前向。所以 GPU 仍然要跑 CNN encoder。

为什么 linear probe 反而 GPU 高？

1. 数据增强少，CPU 不再拖后腿  
   预训练 SimCLR 每张图片要做两次随机增强：`RandomResizedCrop`、`ColorJitter`、`RandomGrayscale` 等，CPU 数据准备比较慢，GPU 经常等数据。  
   Linear probe 通常只做 `ToTensor()`，CPU 很快把 batch 喂给 GPU，所以 GPU 更容易吃满。

2. 每个 batch 的计算更连续  
   Linear probe 是标准监督训练：encoder forward + classifier forward + cross entropy。流程简单，GPU 可以连续算。

3. 你可能 linear probe 训练了 100 轮  
   你的结果文件里是：

   ```text
   linear_probe_epochs: 100
   batch_size: 32
   train_samples: 2000
   ```

   轮数多时，任务持续运行，监控工具更容易看到高负载。

4. 冻结 encoder 不等于 GPU 不工作  
   冻结只是：

   ```python
   param.requires_grad = False
   ```

   它省掉的是 encoder 的反向梯度计算和参数更新，但 encoder 的前向计算仍然存在。

5. 如果代码没有用 `torch.no_grad()` 包住 encoder，显存/计算图开销还会更高  
   更标准的写法是 linear probe 训练时：

   ```python
   with torch.no_grad():
       features = encoder(images)
   logits = classifier(features)
   ```

   这样 encoder 只提特征，不保存计算图。然后只对 classifier 做反向传播。

你可以检查你的 `linear_probe.py` 里是不是类似这样：

```python
features = encoder(images)
logits = classifier(features)
loss = criterion(logits, labels)
loss.backward()
```

如果是这样，即使 encoder 参数冻结了，也可能仍然构建一部分计算图。建议改成：

```python
encoder.eval()

with torch.no_grad():
    features = encoder(images)

logits = classifier(features)
loss = criterion(logits, labels)
```

报告里可以这样写：

```text
Linear probe 阶段 GPU 利用率较高，是因为虽然 encoder 参数被冻结，但每个 batch 仍然需要通过 encoder 前向提取图像特征。同时 linear probe 阶段数据增强较少，CPU 数据加载瓶颈降低，因此 GPU 能够更连续地执行计算。冻结 encoder 只是不更新其参数，并不意味着不使用 GPU 计算 encoder。
```

一句话：预训练 GPU 低，多半是 CPU 增强拖住了；linear probe GPU 高，多半是数据喂得更顺，encoder 前向一直在跑。

---

