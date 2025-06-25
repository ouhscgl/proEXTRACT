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

    try:
        search_path = r'C:\Users\biochemlab\Documents\NIRx\Data'
        for root, dirs, files in os.walk(search_path):
            inf_files = [f for f in files if f.lower().endswith('.inf')]
            for file in inf_files:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    if search_text in content:
                        source_folder = os.path.dirname(full_path)
                        folder_name = search_text + '_NIR_'
                        if 'fingertapping' in content:
                            folder_name += 'FTP'
                        elif 'nback' in content:
                            folder_name += 'NBK'
                        else:
                            print(f'Stimulus uncertain in file {file}.')
                        destination_folder = os.path.join(dest_root, folder_name)
                        try:
                            shutil.copytree(source_folder, 'NIR_DAT', destination_folder)
                            print(f'{source_folder} >>> {destination_folder}')
                        except Exception as e:
                            print(f'Error copying folder {source_folder}: {str(e)}')
                        print(f"Found match in: {full_path}")
                        print('-'*50)
                        
                except Exception as e:
                    print(f"Error reading {full_path}: {str(e)}")
                    continue
    
    except Exception as e:
        print(f"Error accessing directory: {str(e)}")
        return
    else:
        print("\nNo matches found")
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    args = parser.parse_args()
    
    user_input = input('Enter subject ID (e.g.: UTC001_V1): ')
    print('-'*50)
    
    search_inf_files(search_text=user_input, config_path = args.config)