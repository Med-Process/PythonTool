import os
import shutil

# for voc 2007
# voc_train_val_img = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/voc2007/JPEGImages"
# train_txt = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/VOCtrainval_06-Nov-2007/VOCdevkit/VOC2007/ImageSets/Main/train.txt"
# val_txt = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/VOCtrainval_06-Nov-2007/VOCdevkit/VOC2007/ImageSets/Main/val.txt"

# voc_coco_train_target_dir = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/voc2007/train2007"
# voc_coco_val_target_dir = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/voc2007/val2007"


# for voc2012
voc_train_val_img = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/voc2012/JPEGImages"
train_txt = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/ImageSets/Main/train.txt"
val_txt = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/VOCtrainval_11-May-2012/VOCdevkit/VOC2012/ImageSets/Main/val.txt"

voc_coco_train_target_dir = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/voc2012/train2012"
voc_coco_val_target_dir = "/home/ssd_14T/caogp/public_data/VOC07-12/voc_coco/voc2012/val2012"


with open(train_txt, "r") as f:
    train = f.read()
    tp = train.split("\n")
    for j in range(len(tp)):
        file_path = os.path.join(voc_train_val_img, tp[j]+".jpg")
        tar_path = os.path.join(voc_coco_train_target_dir, tp[j]+".jpg")
        if os.path.exists(file_path):
            shutil.move(file_path, tar_path)
        else:
            print("Non-exist file", file_path)

print("Train data splited!...")

with open(val_txt, "r") as f:
    train = f.read()
    tp = train.split("\n")
    for j in range(len(tp)):
        file_path = os.path.join(voc_train_val_img, tp[j]+".jpg")
        tar_path = os.path.join(voc_coco_val_target_dir, tp[j]+".jpg")
        if os.path.exists(file_path):
            shutil.move(file_path, tar_path)
        else:
            print("Non-exist file", file_path)

print("Val data splited!...")