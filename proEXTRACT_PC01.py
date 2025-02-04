#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import re

def search_inf_files(search_paths=None, search_text="NRAXXX_V3", destination_bases=None):
    '''
    Export Manager written for fNIRS Setup v2.0 / [1] PC
    2025.01.30
    '''
    if search_paths is None:
        search_paths = ["C:\\NIRx\\Data"] * 3
    if destination_bases is None:
        destination_bases = ["C:\\NIRx\\Data"] * 3

    # E-Prime file search
    epr_pattern = re.compile(rf"NIRS_Nback \(short\)__NR-in-aging-{search_text[3:6]}-{search_text[-1]}\.(?:txt|html|edat3|xml)$")
    try:
        files = os.listdir(search_paths[0])
        matching_files = [f for f in files if epr_pattern.match(f)]
        if matching_files:
            print(f"Found {len(matching_files)} E-Prime files:")
            for file in matching_files:
                source_path = os.path.join(search_paths[0], file)
                ext = os.path.splitext(file)[1]
                destination_path = os.path.join(destination_bases[0], 
                                                f'{search_text}_NIR_NBK_COG{ext}')
                try:
                    shutil.copyfile(source_path, destination_path)
                    print(f'{source_path} >>> {destination_path}')
                except Exception as e:
                    print(f'Error copying file: {str(e)}')
            print('-'*50)
        else:
            print(f"No matching E-Prime files found for {search_text}")
    except Exception as e:
        print(f"Error accessing folder: {str(e)}")
    
    # EEG file search
    try:
        files = os.listdir(search_paths[1])
        edf_file = [f for f in files if f.startswith(f'{search_text}_EPOCX') and f.endswith('00.edf')]
        csv_file = [f for f in files if f.startswith(f'{search_text}_EPOCX') and f.endswith('_intervalMarker.csv')]
        
        if edf_file and csv_file:
            edf_path = os.path.join(search_paths[1], edf_file[0])
            csv_path = os.path.join(search_paths[1], csv_file[0])
            print(f"Found match in: {edf_file[0]}")
            eeg_dest_path = os.path.join(destination_bases[1], 
                                         f'{search_text}_EEG_NBK_DAT.edf')
            csv_dest_path = os.path.join(destination_bases[1], 
                                         f'{search_text}_EEG_NBK_MRK.csv')
            try:
                shutil.copyfile(edf_path, eeg_dest_path)
                shutil.copyfile(csv_path, csv_dest_path)
                print(f'{edf_path} >>> {eeg_dest_path}')
                print(f'{csv_path} >>> {csv_dest_path}')
                print('-'*50)
            except Exception as e:
                print(f'Error copying file: {str(e)}')
        else:
            print(f"No matching EEG files found for {search_text}")
    except Exception as e:
        print(f"Error accessing folder: {str(e)}")
    
    # MATLAB file search
    mat_patterns = [
        f"{search_text}_SubjectTrialLog.mat",
        f"{search_text}_SubjectTimeLog.mat"]
    try:
        subject_folder = os.path.join(search_paths[2], f'{search_text[:6]}')
        files = os.listdir(subject_folder)
        found_files = []
        for pattern in mat_patterns:
            if pattern in files:
                found_files.append(os.path.join(subject_folder, pattern))
        
        if len(found_files) == 2:
            print(f"Found match in: {subject_folder}")
            str_path = os.path.join(destination_bases[2], 
                                    f'{search_text}_SubjectTrialLog.mat')
            stl_path = os.path.join(destination_bases[2], 
                                    f'{search_text}_SubjectTimeLog.mat')
            try:
                shutil.copyfile(found_files[0], str_path)
                shutil.copyfile(found_files[1], stl_path)
                print(f'{found_files[0]} >>> {str_path}')
                print(f'{found_files[1]} >>> {stl_path}')
                print('-'*50)
            except Exception as e:
                print(f'Error copying file: {str(e)}')
        else:
            print(f"No matching MATLAB files found for {search_text}")
    except Exception as e:
        print(f"Error accessing folder: {str(e)}")

if __name__ == "__main__":
    user_input = input('Enter subject ID (e.g.: UTC001_V1): ')
    print('-'*50)
    search_inf_files(
        search_paths=[
            'C:\\NIRx\\Data',
            'C:\\NIRx\\Data',
            'C:\\NIRx\\Data'
        ],
        search_text=user_input,
        destination_bases=[
            f'C:\\Projects\\{user_input[:3]}',
            f'C:\\Projects\\{user_input[:3]}',
            f'C:\\Projects\\{user_input[:3]}'
        ]
    )