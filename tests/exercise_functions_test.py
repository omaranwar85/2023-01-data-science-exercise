# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:31:50 2023

@author: omar
"""

import os
import sys
  
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  
sys.path.append(parent_path)

from src.exercise_functions import clean_csv_files,visulize_data #clean_csv_files, visulize_data


clean_csv_files(["09"])
visulize_data()