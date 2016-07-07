import openpyxl
import os
from os import listdir
from openpyxl import load_workbook
import string
import matplotlib.pyplot as plt
from openpyxl import Workbook
import plotGraph
from plotGraph import PlotGraph

class PlotCapacity(PlotGraph):
    AreaElectrode = 1
    


    def plot_data(self, file_names, sheet_num, column_cell, set_num,
                  graphTitle, AreaElectrode, 
                  YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
                  YaxisLabel,XaxisLabel):
        
        count =0
        column_name = column_cell[0]
        # add formating code
        for file_name in file_names:
            wb = load_workbook(file_name)
            cur_sheet = wb[sheet_num]
            max_length = cur_sheet.max_row
            end_cell = column_name + str(max_length)
            start_cell = column_name + str(1)
            temp_cell = cur_sheet[start_cell:end_cell]
            capacity = self.extract_data(temp_cell, self.AreaElectrode)       
             
            cycle_number = range(1,max_length)
             
            if count >=set_num or count == 0:
                self.setParam(graphTitle, AreaElectrode, float(YAxisLimit), float(YAxisLower), 
                                    float(XAxisLimit), float(XAxisLower),YaxisLabel,XaxisLabel)                
                count = 1
                            
            plt.plot(cycle_number,capacity)
 
            count +=1
                    
        
        plt.show()
        
 