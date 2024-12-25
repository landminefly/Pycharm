import sys
if len(sys.argv) == 2:
    try:
        epoches = int(sys.argv[1])
        if epoches <= 0:
            raise ValueError
    except ValueError:
        exit('argument must be a num that is greater than zero')
else:
    epoches = 5

from dataPreparation import dataset_path, csv_file
from module import ResNet
from PIL import Image
from torchvision import transforms
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
import os
import csv

print('torch version:', torch.__version__)
print('torch.cuda.is_available:', torch.cuda.is_available())
print("loading data...")
# ------------------------------------------------------------
# 读取csv文件，获取所有图片路径及其对应的标签
# ------------------------------------------------------------

# 保存所有读取的图片路径
images_loaded = []
# 保存所有读取图片对应的标签
labels_loaded = []
if os.path.exists(os.path.join(dataset_path, csv_file)):
    with open(os.path.join(dataset_path, csv_file)) as f:
        # 获取csv reader
        reader = csv.reader(f)
        # 按行读取，将每行中存储的图片路径及其对应标签分别存储到两个列表中
        for row in reader:
            image, label = row
            images_loaded.append(image)
            labels_loaded.append(int(label))

# 确保两个列表的长度对应
assert len(images_loaded) == len(labels_loaded)
print(f"number of images and labels:{len(images_loaded), len(labels_loaded)}")
print(f"a sample of image and corresponding label:{images_loaded[0], labels_loaded[0]}")


# ------------------------------------------------------------
# 定义自定义数据集类
# ------------------------------------------------------------

class MyDataset(Dataset):
    def __init__(self, images_loaded, labels_loaded, resize, mode):
        self.x = images_loaded
        self.y = labels_loaded
        self.resize = resize
        # 以6:2:2的比例分割train、dev、train子集
        if mode == 'train':
            self.x = self.x[:int(0.6 * len(self.x))]
            self.y = self.y[:int(0.6 * len(self.y))]
        elif mode == 'dev':
            self.x = self.x[int(0.6 * len(self.x)):int(0.8 * len(self.x))]
            self.y = self.y[int(0.6 * len(self.y)):int(0.8 * len(self.y))]
        elif mode == 'train':
            self.x = self.x[int(0.8 * len(self.x)):]
            self.y = self.y[int(0.8 * len(self.y)):]

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        image, label = Image.open(self.x[index]).convert('RGB'), self.y[index]
        # 在返回图像之前，先对其应用图像增强，增加数据集的多样性
        # 还要调整图像的大小，使其符合神经网络的输入要求，这里将传入的resize参数作为调整后的图像大小
        transform = transforms.Compose([
            # 图像增强、大小调整
            transforms.Resize(int(self.resize * 1.25)),
            transforms.RandomRotation(30),
            transforms.CenterCrop(self.resize),
            # 转化为tensor
            transforms.ToTensor(),
            # 归一化，这里的均值和方差数据来源于统计数据
            transforms.Normalize(mean = [0.485, 0.456, 0.406],
                                 std = [0.229, 0.224, 0.225])
        ])
        image = transform(image)
        # 返回图像张量及其标签
        return image, label


# ------------------------------------------------------------
# 加载数据集
# ------------------------------------------------------------

batch_size = 32

train_set = MyDataset(images_loaded, labels_loaded, 224, 'train')
dev_set = MyDataset(images_loaded, labels_loaded, 224, 'dev')
test_set = MyDataset(images_loaded, labels_loaded, 224, 'test')

train_loader = DataLoader(train_set, batch_size = batch_size, shuffle = True)
dev_loader = DataLoader(dev_set, batch_size = batch_size, shuffle = True)
test_loader = DataLoader(test_set, batch_size = batch_size, shuffle = True)

cuda = torch.device('cuda')


# ------------------------------------------------------------
# 定义训练和评估函数
# ------------------------------------------------------------

# 评估函数，传入模型、数据集、Loss函数，返回loss值和acc率
def evaluate(model, loader, criteon):
    correct_count = 0
    total_count = 0
    total_loss = 0

    for batch_idx, (x, y) in enumerate(loader):
        x, y = x.to(cuda), y.to(cuda)
        y_hat = model(x)

        total_loss += criteon(y_hat, y)

        pred = y_hat.argmax(dim = 1)
        correct_count += torch.eq(pred, y).sum().float().item()
        total_count += len(y)

    acc = correct_count / total_count
    total_loss = total_loss / len(loader)
    return acc, total_loss


# 训练函数
def train():
    # 获取tensorboard的SummaryWriter对象，后面要使用该对象将数据记录到tensorboard中
    # log_dir指定数据的保存路径，flush_secs指定多少秒将数据写入到本地一次（默认为120）
    writer = SummaryWriter(log_dir = "logs/result_1", flush_secs = 120)
    # 获取模型对象
    model = ResNet(5).to(cuda)
    # 定义训练次数、优化器等内容
    optimizer = torch.optim.Adam(model.parameters(), weight_decay = 0.3)
    criteon = nn.CrossEntropyLoss().to(cuda)
    # 记录对dev_set评估得到的最高acc值及其对应的epoch
    best_dev_acc, best_dev_epoch = 0, 0

    for epoch in range(epoches):
        # 在train_set上训练
        model.train()
        correct_count = 0
        total_count = 0
        loss_train = 0
        acc_train = 0

        for batch_idx, (x, y) in enumerate(train_loader):
            x, y = x.to(cuda), y.to(cuda)
            y_hat = model(x)
            loss = criteon(y_hat, y)
            loss_train += loss

            pred = y_hat.argmax(dim = 1)
            correct_count += torch.eq(pred, y).sum().float().item()
            total_count += len(y)

            # 梯度下降
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # 计算train_set的loss值、acc率，并记录到tensorboard中
        loss_train = loss_train / len(train_loader)
        acc_train = correct_count / total_count
        writer.add_scalar(tag = 'Loss/train',
                          scalar_value = loss_train,
                          global_step = epoch)
        writer.add_scalar(tag = 'Acc/train',
                          scalar_value = acc_train,
                          global_step = epoch)
        print(f'epoch:{epoch}\t train_loss:{loss_train.item()}\t train_acc:{acc_train}')


        model.eval()
        acc_dev, loss_dev = evaluate(model, dev_loader, criteon)
        print(f'epoch:{epoch}\t dev_loss:{loss_dev.item()}\t dev_acc:{acc_dev}')
        if acc_dev > best_dev_acc:
            best_dev_acc = acc_dev
            best_dev_epoch = epoch
            torch.save(model.state_dict(), './state/best.mdl')

    # 训练结束后，加载保存的模型参数，并在test_dev上评估
    print('training ends')
    model.load_state_dict(torch.load('./state/best.mdl'))
    print('loaded from checkpoint')
    model.eval()
    acc_test, loss_test = evaluate(model, test_loader, criteon)
    print(f'epoch:{best_dev_epoch}\t test_loss:{loss_test.item()}\t test_acc:{acc_test}')


# ------------------------------------------------------------
# 开始训练
# ------------------------------------------------------------

print('start training...')
train()