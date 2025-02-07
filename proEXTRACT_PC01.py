#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import re
import sys
import argparse
import json

def search_inf_files(search_text="NRAXXX_V3", config_path=None):
    '''
    Export Manager written for fNIRS Setup v2.0 / [1] PC
    2025.01.30 @ZBK
    '''
    if config_path is None:
       print('Please provide a config file.')
       return
    else:
        try:
            with open(config_path,'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error accessing config file: {str(e)}")
            return

    dest_root = config['destination_base'].format(
        subject_prefix = search_text[:3])    

    # E-Prime file search
    eprime_config = config['file_patterns']['eprime']
    base_pattern  = eprime_config['base_pattern'].format(
        subject_num = f"0*{search_text[4:6]}",
        version = search_text[-1])
    epr_pattern = re.compile(base_pattern)
    try:
        files = os.listdir(config['search_paths']['eprime'])
        matching_files = [f for f in files if epr_pattern.search(f)]
        if matching_files:
            print(f"Found {len(matching_files)} E-Prime files:")
            for file in matching_files:
                source_path = os.path.join(config['search_paths']['eprime'],
                                           file)
                ext = os.path.splitext(file)[1]
                destination_path = os.path.join(dest_root, 'NIR_COG', 
                                                f'{search_text}_NIR_NBK_COG{ext}')
                try:
                    shutil.copyfile(source_path, destination_path)
                    print(f'{source_path} >>> {destination_path}')
                except Exception as e:
                    print(f'Error copying file: {str(e)}')
            print('-'*50)
        else:
            print(f"No matching E-Prime files found for {search_text}")
            print('-'*50)
    except Exception as e:
        print(f"Error accessing folder: {str(e)}")
    
    # EEG file search
    try:
        files = os.listdir(config['search_paths']['eeg'])
        edf_file = [f for f in files if f.startswith(f'{search_text}_EPOCX') and f.endswith('00.edf')]
        csv_file = [f for f in files if f.startswith(f'{search_text}_EPOCX') and f.endswith('_intervalMarker.csv')]
        
        if edf_file and csv_file:
            edf_path = os.path.join(config['search_paths']['eeg'], edf_file[0])
            csv_path = os.path.join(config['search_paths']['eeg'], csv_file[0])
            print(f"Found match in: {edf_file[0]}")
            eeg_dest_path = os.path.join(dest_root, 'EEG_DAT', 
                                         f'{search_text}_EEG_NBK_DAT.edf')
            csv_dest_path = os.path.join(dest_root, 'EEG_DAT',  
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
            print('-'*50)
    except Exception as e:
        print(f"Error accessing folder: {str(e)}")
    
    # MATLAB file search
    mat_patterns = [
        f"{search_text}_SubjectTrialLog.mat",
        f"{search_text}_SubjectTimeLog.mat"]
    try:
        subject_folder = os.path.join(config['search_paths']['matlab'], 
                                      f'{search_text[:6]}')
        files = os.listdir(subject_folder)
        found_files = []
        for pattern in mat_patterns:
            if pattern in files:
                found_files.append(os.path.join(subject_folder, pattern))
        
        if len(found_files) == 2:
            print(f"Found match in: {subject_folder}")
            str_path = os.path.join(dest_root, 'EEG_COG',
                                    f'{search_text}_SubjectTrialLog.mat')
            stl_path = os.path.join(dest_root, 'EEG_COG',
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
            print('-'*50)
    except Exception as e:
        print(f"Error accessing folder: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    args = parser.parse_args()
    
    user_input = input('Enter subject ID (e.g.: UTC001_V1): ')
    print('-'*50)
    
    search_inf_files(search_text=user_input, config_path = args.config)