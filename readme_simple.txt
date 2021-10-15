dialog1:
	datasets:1.相关文件夹带中文，需要rename
	              2.标注文件是TXT格式，不需要使用相关annotation.py来做格式转换
	              3.与实现模型所用的数据集的格式不同，需要做更改
	steps:(1)调用rename()，主函数要根据使用的实际数据集格式更改
	         (2)调用split_datasets(),完成数据集的分割。暂时确定，train = 所有图片， val = 第一小类， test = 第一小类
	         (3)调用annotations_extraction(),将图像地址与相应标注抓取到txt文件。手动删除文件年份
	         (4)调整yolov3.cfg,此文件用于转换.weights文件.主要是batch, fileter,class
	         (5)修改model_data下的coco_classes和voc_classes。(为什么要改这两个文件)
	         (6)修改yolo3下的model.py, 将类别max_boxes改成当前数据集要分的类别
	         (7)运行train.py

	problem:(1)图像没有目标，标注文件为空，这导致生成的图片路径+标注信息格式错误