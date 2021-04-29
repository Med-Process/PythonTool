import os
import pydicom
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

import shutil

ATTRIBUTE = [
    # patient
    (0x00100010, 'PN', '***'),
    (0x00101001, 'PN', '***'),
    (0x00101000, 'LO', '***'),
    (0x00101040, 'ST', '***'),
    
    # institution
    (0x00080080, 'LO', '***'),
    (0x00080081, 'ST', '***'),
    
    # other name
    (0x00080090, 'PN', '***'),
    (0x00081050, 'PN', '***'),
    (0x00081070, 'PN', '***'),
]

EXTEN = ['.txt', '.png', '.doc', '.xml', '.jpg', '.jpeg', '.docx']


def anonymize(data_dir, save_dir, logger=None, i=None):
    state = None
    if i is not None and not i%10:
        print('Process: ', i)
    num = 0
    for root, _, files in os.walk(data_dir):
        for f in files:
            if os.path.splitext(f)[-1] not in EXTEN:
                try:
                    src_path = os.path.join(root, f)
                    ds = pydicom.dcmread(src_path)
                    for tag, vr, v in ATTRIBUTE:
                        ds[tag] = pydicom.DataElement(tag, vr, v)

                    save_path = src_path.replace(data_dir, save_dir)
                    # save_path = os.path.join(save_dir, ds.PatientID, ds.StudyDate, ds.StudyInstanceUID, ds.SeriesInstanceUID, str(ds.InstanceNumber)+'.dcm')
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    ds.save_as(save_path)


                except Exception as e:
                    state = 'PT_DT_0001'
                    if logger is not None:
                        logger.info("\n")
                        logger.info(state+ ": " + str(e))
                        logger.info("Error path: ", os.path.join(root, f))
                    # else:
                    #     print("Error path: ", os.path.join(root, f))
                    
    return state
    

def anonymize_multi_process(data_dir, save_dir, num_proc=8):
    pool = ProcessPoolExecutor(num_proc)
    fns = os.listdir(data_dir)
    print('Num of fns: ', len(fns))
    for i, fn in enumerate(fns):
        study_path = os.path.join(data_dir, fn)
        future = pool.submit(anonymize, study_path, save_dir, i)
    pool.shutdown(wait=True)


def anonymize_csv(csv_path, data_dir, save_dir, num_proc=8):
    pids = pd.read_csv(csv_path)['pid_fn']
    pids = list(set(pids))
    if num_proc<=1:
        for pid in pids:
            path = os.path.join(data_dir, str(pid))
            anonymize(path, save_dir)
    else:
        pool = ProcessPoolExecutor(num_proc)
        for i, pid in enumerate(pids):
            path = os.path.join(data_dir, str(pid))
            pool.submit(anonymize, path, save_dir, i)
        pool.shutdown(wait=True)


if __name__ == '__main__':
    data_dir = ""
    save_dir = ""
    anonymize(data_dir, save_dir)
    # anonymize_multi_process(data_dir, save_dir, num_proc=4)

