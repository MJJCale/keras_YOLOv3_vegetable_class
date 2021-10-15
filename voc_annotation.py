####################################################
##实现XML标注转换为TXT标注.生成三个txt文件，train,val,test
##相应的标注文件写到VOCdevkit同一个目录下
####################################################

import xml.etree.ElementTree as ET
from os import getcwd

#将要生成的三个文件，可以改年份,其他最好不变
sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
#本次训练的分类总数.在人类未涉足的领域用无监督，其他的AI要与人类一致
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert_annotation(year, image_id, list_file):
    #从这里的地址可以看出，为什么在训练本地数据集时要设计VOCdevkit/VOC2021这样的结构
    #为了使用模型中写好的函数，对不同的网络可以写不同的文件结构
    #就是说模仿这个模型使用的数据集的结构
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(wd, year, image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

print('完成XML格式标注向TXT格式标注的转换，继续你的表演，少年！！！！')
