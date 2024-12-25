import csv
import glob
import os
import random

print("preparing data...")
# ------------------------------------------------------------
# 获取所有分类，并建立分类结果与其对应数字（即标签）的映射字典
# ------------------------------------------------------------

name2label = {}
# 如果缺失pokemon中的数据集，可从百度网盘上下载
dataset_path = 'pokemon'
# 列出代表不同分类结果的所有目录
# 因为os.listdir()返回目录的顺序是不确定的，因此要对返回结果进行排序，以保证每个分类结果所对应的数字是确定的
for name in sorted(os.listdir(os.path.join(dataset_path))):
    # 确保name对应的是目录而不是文件
    if os.path.isdir(os.path.join(dataset_path, name)):
        # 从0开始，为不同分类结果分配数字标签，并建立映射关系保存到字典中
        name2label[name] = len(name2label.keys())

# 查看结果
print(f"name2label: {name2label}")

# ------------------------------------------------------------
# 创建一个csv文件，该文件保存了训练集中所有图片路径及其对应的标签
# ------------------------------------------------------------

# 保存所有图片路径的列表
images_path = []
for name in name2label.keys():
    # 这里的glob()返回一个列表，包括了name目录下所有后缀为jpg的文件路径，下同
    images_path += glob.glob(os.path.join(dataset_path, name, '*.jpg'))
    images_path += glob.glob(os.path.join(dataset_path, name, '*.jpeg'))
    images_path += glob.glob(os.path.join(dataset_path, name, '*.png'))
    images_path += glob.glob(os.path.join(dataset_path, name, '*.gif'))
# 打乱images_path
random.shuffle(images_path)
print(f"number of images: {len(images_path)}")
print(f"a sample of images path: {images_path[0]}")

csv_file = 'dataset.csv'
if not os.path.exists(os.path.join(dataset_path, csv_file)):
    # 将图片路径及其对应标签写入csv文件
    with open(os.path.join(dataset_path, csv_file), mode = 'w', newline = '') as f:
        # 获取csv writer
        writer = csv.writer(f)
        # 遍历获取每张图片对应的标签，并将该图片路径及其对应标签写入文件
        for img_path in images_path:
            # 将系统分隔符（Linux为'/'，Windows为'\\'）将图片路径进行分割，分割后的倒数第二个元素就是图片对应的分类结果
            # 例：'pokemon\\bulbasaur\\00000183.jpg'，分割后的倒数第二个元素是bulbasaur
            name = img_path.split(os.sep)[-2]
            label = name2label[name]
            writer.writerow([img_path, label])
        print(f'images and corresponding labels have been successfully written into this file: {os.path.join(dataset_path, csv_file)}')
