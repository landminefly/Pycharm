import os
import re
import numpy as np
import matplotlib.pyplot as plt


def main():
    # 读取文件，分词后存储到contents中
    root = 'dataset'
    contents = []
    for name in sorted(os.listdir(os.path.join(root))):
        with open(os.path.join(root, name), 'r', encoding = 'utf-8') as f:
            content = f.read()
            content = re.sub(r'\W', ' ', content).lower().split()
            contents.append(content)

    # 建立字典，记录每个单词在各篇文章的出现次数
    word_dict = {}
    for idx, content in enumerate(contents):
        for i in content:
            if i not in word_dict.keys():
                word_dict[i] = [0] * len(contents)
                word_dict[i][idx] = 1
            else:
                word_dict[i][idx] += 1

    # 建立tf_idf值字典，记录每个单词的tf、idf值
    tf_idf_dict = {}
    for i in word_dict.keys():
        total_count = 0
        non_zero_count = 0
        for count in word_dict[i]:
            total_count += count
            if count != 0:
                non_zero_count += 1
        tf = 1 + np.log2(total_count)
        idf = np.log2(len(contents) / non_zero_count)
        tf_idf_dict[i] = [tf, idf]

    # 根据tf值排序
    tf_idf_dict = dict(sorted(tf_idf_dict.items(), key = lambda item: item[1][0], reverse = True))

    # 建立绘制图表所需的数据
    x = []
    y_tf = []
    y_idf = []
    y_tf_idf = []

    # x轴数据
    x = np.arange(len(word_dict.keys()))
    # y轴数据
    for i in tf_idf_dict.keys():
        y_tf.append(tf_idf_dict[i][0])
        y_idf.append(tf_idf_dict[i][1])
        y_tf_idf.append(tf_idf_dict[i][0] * tf_idf_dict[i][1])

    # 绘制散点图
    plt.figure(figsize = (16, 8))
    # 绘制图表1
    plt.subplot(121)
    line_1 = plt.scatter(x, y_tf, c = 'blue', marker = '*', s = 10)
    line_2 = plt.scatter(x, y_idf, c = 'red', marker = '+', s = 10)
    plt.legend(handles = [line_1, line_2], labels = ['tf', 'idf'])
    plt.xlabel('n')
    plt.ylabel('value')
    # 绘制图表2
    plt.subplot(122)
    line_3 = plt.scatter(x, y_tf_idf, c = 'black', marker = '*', s = 10)
    plt.legend(handles = [line_3], labels = ['tf*idf'])
    plt.xlabel('n')
    plt.ylabel('value')
    # 保存矢量图
    plt.savefig('graph.svg', format = 'svg')
    # 显示图表
    plt.show()


if __name__ == '__main__':
    main()
