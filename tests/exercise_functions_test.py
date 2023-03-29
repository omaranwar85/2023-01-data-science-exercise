# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:31:50 2023

@author: omar
"""

import os
import sys
  
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  
sys.path.append(parent_path)

from src/exercise_functions import clean_csv_files,visulize_data #clean_csv_files, visulize_data

clean_csv_files()     #Call to function to generate clean scv files for all 4 months
######visulize_data()       #Visulaise data for (default) 6th month, with a filter of (default) size: 7x7