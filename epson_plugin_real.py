"""
Copyright (C) {2021}  {Corporate Delinquents Motorcycle Club, outragebeyound & Loafter}
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
"""


import os
import pydicom
import datetime


def folder_surfer():
    rootdir = r'C:\DBurner\input'
    with os.scandir(rootdir) as fd:
        for folder in fd:
            if not folder.is_dir() or len(os.listdir(folder)) == 0:
                continue
            with os.scandir(folder) as f:
                if any(file.is_file() and file.name == 'readytoburn' and not len(os.listdir(os.path.join(rootdir, folder.name,'IMAGES')))==0 for file in f):  # Maybe not needed? use os.path.exists(rootdir+readyroburn)
                    directory = os.path.join(rootdir, folder.name)
                    create_jdf_file(folder.name, directory)


def get_dicom_data(directory):
    first_dicom = return_first_dicom_from_folder(directory)
    ds = pydicom.read_file(first_dicom)
    study_descr = str(ds.StudyDescription)
    pat_name = str(ds.PatientName)
    modality = return_modality(directory)
    study_date_dt = datetime.datetime.strptime(str(ds.StudyDate), '%Y%m%d')    
    pat_id = str(ds.PatientID)
    study_date = datetime.date.strftime(study_date_dt, "%d.%m.%Y")   
    return study_descr, pat_name, study_date, modality, pat_id


def create_merge_bat(directory):
    os.chdir(directory)
    dicom_data = get_dicom_data(directory)
    with open('print.dat', 'w') as file_object:
        file_object.write(f'Study_descr={dicom_data[0]}\nPat_name={dicom_data[1]}\nStudy_date={dicom_data[2]}\nModality={dicom_data[3]}\nPat_id={dicom_data[4]}')


def create_jdf_file(name, directory):
    create_merge_bat(directory)
    os.chdir(r'C:\EPSON\TDBridge\Orders')
    filename = "%s.jdf" % name
    with open(filename, 'w') as file_object:
        file_object.write(
            f"COPIES=1\nDATA={directory}\nPUBLISHER=PP100\nDISC_TYPE=DVD\nFORMAT=UDF102\nLABEL=C:\\DBurner\\bin\\herzendvd.tdd\nREPLACE_FIELD={os.path.join(directory, 'print.dat')}")
    os.rename(os.path.join(directory, 'readytoburn'), os.path.join(directory, 'jdf_created'))


def return_first_dicom_from_folder(directory):
    dicom_dir = os.path.join(directory, 'IMAGES')
    for file in os.listdir(dicom_dir):
        try:
            pydicom.read_file(os.path.join(dicom_dir, file))
        except pydicom.errors.InvalidDicomError:
            continue
        return os.path.join(dicom_dir, file)

def return_modality(directory):
    dicom_dir = os.path.join(directory, 'IMAGES')
    modality = set()
    with os.scandir(dicom_dir) as d:
        for file in d:
            try:
                ds = pydicom.read_file(file)
                modality_tag = str(ds.Modality)
                modality.add(modality_tag)                
            except pydicom.errors.InvalidDicomError:
                continue            
    modality_print = ','.join(modality)
    return modality_print


folder_surfer()
