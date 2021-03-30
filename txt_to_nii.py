import os
import glob
import numpy as np
import SimpleITK as sitk
from scipy.ndimage import zoom

# 该文件用于将MIMICS软件导出的肺叶分割结果（txt格式），转化为其他可读格式（nii）


def write_nii(save_dir, image_zyx, spacing_zyx, name="npz"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    spacing_xyz = spacing_zyx[::-1]
    img_sitk = sitk.GetImageFromArray(image_zyx)
    img_sitk.SetSpacing(spacing_xyz)
    sitk.WriteImage(img_sitk, os.path.join(
        save_dir, name + '.nii.gz'))


def draw_mask(mask_zyx, points_xyz, origin_xyz, spacing_xyz, label=1):
    shape = mask_zyx.shape
    for p in points_xyz:
        p_pixel = np.abs(np.array(p[:3]) - origin_xyz) / spacing_xyz
        p_pixel = np.rint(p_pixel).astype(int)
        x,y,z = p_pixel

        if z < shape[0] and y < shape[1] and x < shape[2]:
            mask_zyx[z,y,x] = label

    return mask_zyx


def point2nii(file_dir, image_path, img_save_dir, mask_save_dir):
    # file_pathes = glob.glob(os.path.join(file_dir, '*.txt'))
    file_pathes = [file_dir + ".txt"]

    if os.path.isfile(image_path):
        img_sitk = sitk.ReadImage(image_path)
    else:
        reader = sitk.ImageSeriesReader()
        img_names = reader.GetGDCMSeriesFileNames(image_path)
        print("The dicom image number is: " + str(len(img_names)))
        reader.SetFileNames(img_names)
        img_sitk = reader.Execute()

    image_zyx = sitk.GetArrayFromImage(img_sitk)
    spacing_xyz = np.array(img_sitk.GetSpacing())
    origin_xyz = np.array(img_sitk.GetOrigin())
    
    mask_zyx = np.zeros_like(image_zyx).astype(np.uint8)

    label_dict = {
        'Airway_grayvalues': 1,
    }

    for file_path in file_pathes:
        try:
            points_xyz = np.loadtxt(file_path, delimiter=',')
        except:
            points_xyz = np.loadtxt(file_path)

        fn = os.path.splitext(os.path.basename(file_path))[0]
        mask_zyx = draw_mask(mask_zyx, points_xyz, origin_xyz, spacing_xyz, 1)
    
    fn = os.path.split(image_path)[-1]
    write_nii(mask_save_dir, mask_zyx, spacing_zyx=spacing_xyz[::-1], name=fn)
    write_nii(img_save_dir, image_zyx, spacing_zyx=spacing_xyz[::-1], name=fn)
    print("Save one nii image successed!...")


if __name__ == '__main__':
    # 用于单个文件夹的文件生成
    file_dirs = "E:/2021/NLST_Airway"     # txt文件路径
    image_dirs= "E:/2021/NLST_Airway/"               # 原图像文件路径，用于读取图像信息


    fns = os.listdir(file_dirs)
    for fn in fns:
        if fn.endswith(".txt"):
            file_name = fn[:-4]
            file_dir = os.path.join(file_dirs, file_name)
            image_path = os.path.join(image_dirs, file_name)

            img_save_dir = 'E:/2021/NLST_Airway/' + file_name + '/img'   # 用于保存未裁剪的原始图像
            mask_save_dir = 'E:/2021/NLST_Airway/' + file_name + '/mask'    # 用于保存未裁剪的原始mask
            if not os.path.exists(img_save_dir):
                os.mkdir(img_save_dir)
            if not os.path.exists(mask_save_dir):
                os.mkdir(mask_save_dir)
            try:
                point2nii(file_dir, image_path, img_save_dir, mask_save_dir)
            except:
                print("Error: ", fn)
