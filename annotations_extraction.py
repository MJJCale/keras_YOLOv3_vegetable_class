############################################
#当前数据集的标注存放在txt文件，并且与同名图片成对存在同一个文件夹下
#按照一个格式提取相应的标注信息
#图片存放的绝对路径 标注1 类别2 标注2 类别2 ...
#提取出的信息放到train, val, test
##############################################

import os
from os import getcwd
import glob
from convert_bbox_for_anno_extraction import convert_bbox

#将要生成的三个文件，可以改年份,其他最好不变
sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

#按照上一步对数据集的划分结果，即按照Main生成的4个txt文件(里面全是文件名，不带后缀)
#中的顺序提取标注中的信息。还是那个问题，本数据集的图片、标注均不在一个文件夹
#这带来了麻烦，当前只采用简便处理。就把第一类当作验证集
wd = getcwd()#当前文件的绝对路径

#遍历数据集获得每个小类的数据总数
path = os.path.join(wd, 'VOCdevkit', 'VOC2007', 'JPEGImages')
files = os.listdir(path)
num = list()
num.append(0)#num[1]对应第一小类的数据总量，num[0] = 0是为了程序上的方便
class_datasets = 2
flag = 0
for fl in files:
    path1 = os.path.join(path,fl,'*.jpg')
    files_2 = glob.glob(path1)
    num.append(len(files_2) + num[flag])
    flag += 1   

for year, image_set in sets:
    #打开Main下的分割好的相关数据集(里面全是文件名，不带后缀),这样就不需要去JPEGImages
    #因为图片和标注文件重名这个缘故
    image_ids = open('VOCdevkit//VOC%s//ImageSets//Main//%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    count = 0#记录当前取了多少张图片
    for image_id in image_ids:
        
        count += 1
        #又是因为标注、图片分了小类，因此必须获得每个小类的总数
        #根据每个小类得数量
        for k in range(class_datasets):
            if count>num[k] and count<=num[k+1]:
                list_file.write('%s\VOCdevkit\VOC%s\JPEGImages\%s\%s.jpg '%(wd, year, k+1,image_id))
                #进入第i+1小类中去找相应的标注文件
                annotation_txt_file = open('%s//VOCdevkit//VOC%s//JPEGImages//%s//%s.txt'%(wd, year, k+1,image_id), 'r')

                #file1将txt文件按行读取，每行内容读出为string
                annotation_txt_file1 = annotation_txt_file.readlines()
                for i in range(len(annotation_txt_file1)):
                    #对行字符串按空格进行拆分
                    annotation_txt_file2 = annotation_txt_file1[i].split()
                    
                    #先替换换行符.python规定，字符串一旦生成就不允许更改
                    #使用索引更换会报错。对字符串使用replace()即可
                    annotation_txt_file2[-1].replace('\n', '')


                    #可能需要对bbox的值进行换算
                    bbox = convert_bbox(annotation_txt_file2)
                    
                    #print('annotation_txt_file2   ', annotation_txt_file2)
                    if i != len(annotation_txt_file1)-1:
                        list_file.write(str(bbox[0])+',')
                        list_file.write(str(bbox[1])+',')
                        list_file.write(str(bbox[2])+',')
                        list_file.write(str(bbox[3])+',')
                        list_file.write(annotation_txt_file2[0]+' ')
                    else:
                        list_file.write(str(bbox[0])+',')
                        list_file.write(str(bbox[1])+',')
                        list_file.write(str(bbox[2])+',')
                        list_file.write(str(bbox[3])+',')
                        list_file.write(annotation_txt_file2[0]+'\n')
                
                break
            else:
                continue

    list_file.close()        

print('图像绝对路径以及对应标注全部提取完毕。请继续你的旅途，少年！前路漫漫，荡涤障碍！')
        
        

