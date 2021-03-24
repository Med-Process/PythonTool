"""
用于测试ASD: Average Surface Distance,并记录在表格中
"""

import os
import csv
import sys

import SimpleITK as sitk
import numpy as np


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from ASD.compute_asd import compute_surface_distances, compute_average_surface_distance

path = "../mask"  # 待测试的mask

d1 = '01liuzhiqiao'   # 对应的数据文件夹


d2 = 'gt'

tp_all_1 = "mask1"
tp_all_2 = "mask2"
tp_all_3 = "mask3"
tp_all_4 = "gt"

doctor_1 = os.path.join(path, d1)
doctor_2 = os.path.join(path, d2)

dc_tp_1 = os.path.join(path, tp_all_1)
dc_tp_2 = os.path.join(path, tp_all_2)
dc_tp_3 = os.path.join(path, tp_all_3)
dc_tp_4 = os.path.join(path, tp_all_4)

mask_dirs = os.listdir(doctor_1)

def writeCsv(csfname,rows):
    with open(csfname, 'a', newline='') as csvf:
        filewriter = csv.writer(csvf)
        filewriter.writerow(rows)

csv_output = d1 + "_" + d2 + ".csv"  # 输出的文件名
doc = ['Doctor', '1: ' + d1 + '  and  2: ' + d2, ]
text = ['Data', 'ASSD']

writeCsv(csv_output, doc)
writeCsv(csv_output, text)

result_list = []

for i in range(len(mask_dirs)):
    file_name = mask_dirs[i]

    d1_full = os.path.join(doctor_1, file_name)
    d2_full = os.path.join(doctor_2, file_name)

    temp_1 = os.path.join(dc_tp_1, file_name)
    temp_2 = os.path.join(dc_tp_2, file_name)
    temp_3 = os.path.join(dc_tp_3, file_name)
    temp_4 = os.path.join(dc_tp_4, file_name)

    if os.path.exists(d1_full) and os.path.exists(d2_full) and os.path.exists(temp_1) and \
            os.path.exists(temp_2) and os.path.exists(temp_3) and os.path.exists(temp_4):
        mask1 = sitk.ReadImage(d1_full)
        spacing = mask1.GetSpacing()
        mask1 = sitk.GetArrayFromImage(mask1)

        mask2 = sitk.ReadImage(d2_full)
        mask2 = sitk.GetArrayFromImage(mask2)

        spac = [spacing[2], spacing[1], spacing[0]]

        # for background
        distance = compute_surface_distances(mask1 == 1, mask2 == 1, spac)
        actual_average_surface_distance = compute_average_surface_distance(distance)

        print(actual_average_surface_distance)
        text_tp = [file_name, round((actual_average_surface_distance[0] + actual_average_surface_distance[1])/2.0, 4)]
        result_list.append(round((actual_average_surface_distance[0] + actual_average_surface_distance[1])/2.0, 4))
        writeCsv(csv_output, text_tp)

mean = np.mean(result_list)
std = np.std(result_list)
max_ = np.max(result_list)
min_ = np.min(result_list)

text_mean = ['Mean', round(mean, 4)]
text_std = ['Std', round(std, 4)]
text_max = ['Max', round(max_, 4)]
text_min = ['Min', round(min_, 4)]

writeCsv(csv_output, text_mean)
writeCsv(csv_output, text_std)
writeCsv(csv_output, text_max)
writeCsv(csv_output, text_min)

print("**********  end  ***********")
