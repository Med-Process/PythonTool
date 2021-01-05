# ### fill hold 用来填充空洞###

import os
import SimpleITK as sitk
import copy
import numpy as np
import cv2

path = 'F:/2021/EXA09/label/'    
save_dir = 'F:/2021/EXA09/label_fill_hole/'
filelist = [file for file in os.listdir(path)]

for fname in filelist:
    print (fname)
    img_itk = sitk.ReadImage(os.path.join(path,fname))
    img_arr = sitk.GetArrayFromImage(img_itk)  #zyx
    spacing = img_itk.GetSpacing()
    img_pred_arr = np.zeros_like(img_arr).astype(np.uint8)

    # 1 'leftu', 2 'leftl', 3 'rightu', 4 'rightm', 5 'rightl', 6 'Airway'
    for i in range(1,6):
        for j in range(img_arr.shape[0]):
            data = copy.deepcopy(img_arr[j])
            data[data != i] = 0
            data[data != 0] = 255
            data_floodfill = data.copy()
            h,w = data_floodfill.shape
            mask = np.zeros((h+2, w+2), np.uint8)
            cv2.floodFill(data_floodfill, mask, (0,0), 255)
            data_floodfill_inv = cv2.bitwise_not(data_floodfill)
            data_out = data | data_floodfill_inv

            img_pred_arr[j][data_out == 255] = i


    img_pred_sitk = sitk.GetImageFromArray(img_pred_arr)
    img_pred_sitk.SetSpacing(spacing)
    sitk.WriteImage(img_pred_sitk, os.path.join(save_dir, fname))
