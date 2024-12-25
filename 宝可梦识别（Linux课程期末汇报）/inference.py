import sys

if len(sys.argv) == 2:
    image_path = sys.argv[1]
else:
    exit('missing arguments: image_path')

import numpy as np
from module import ResNet
from PIL import Image
from torchvision import transforms
import torch
from dataPreparation import name2label

print('torch version:', torch.__version__)
print('torch.cuda.is_available:', torch.cuda.is_available())

# 读取图像
image = Image.open(image_path).convert('RGB')
transform = transforms.Compose([
    # 图像大小调整
    transforms.Resize(int(224)),
    transforms.CenterCrop(224),
    # 转化为tensor
    transforms.ToTensor(),
])
image = transform(image)
image = image.reshape(1, 3, 224, 224)
# 加载模型
cuda = torch.device('cuda')
model = ResNet(5).to(cuda)
model.load_state_dict(torch.load('./state/best.mdl'))
# 开始推理
print('model loaded')
print('start inference...')
y_hat = model(image.to(cuda))

# 查看结果
print('inference done, output: ', y_hat.cpu().detach().numpy())
for label in sorted(name2label.keys()):
    if name2label[label] == np.argmax(y_hat.cpu().detach().numpy()):
        print('result: ', label)
