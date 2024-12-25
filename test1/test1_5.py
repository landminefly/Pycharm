import torch
from torch.utils.data import Dataset, DataLoader


# 假设你有一个自定义的Dataset
class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    # 创建Dataset实例


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dataset = MyDataset(data)

# 创建数据加载器，指定批次大小
batch_size = 2
data_loader = DataLoader(dataset, batch_size = batch_size)

# 现在你可以迭代数据加载器来获取批次数据
for batch_data in enumerate(data_loader):
    print(batch_data)  # 输出: [1, 2], [3, 4], [5, 6], [7, 8], [9, 10]
