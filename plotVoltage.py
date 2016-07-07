import openpyxl
import os
import plotGraph
from os import listdir
from openpyxl import load_workbook
import string
import matplotlib.pyplot as plt

class PlotVoltage(plotGraph):
    AreaElectrode = 1
    
    
    def setParam(self, graphTitle, AreaElectrode, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, YaxisLabel,XaxisLabel):
        #do I need to declare first?
        plt.figure()
        plt.ylabel(YaxisLabel)
        plt.xlabel(XaxisLabel)
        plt.axis([YAxisLower,YAxisLimit,XAxisLower,XAxisLimit])
        plt.title(graphTitle) 
        self.AreaElectrode = AreaElectrode
        
    def breakCycles(self, filenames, sheetName, voltage, capacity):
        #returns inidividual cycles of filenames selected
        dictCyclesNum ={}
        
        for file in filenames:
            comp = file[-4:] 
            if (comp =='xlsx'):
                wb = load_workbook(file, data_only= True)
            
            curSheet = wb[sheetName]
            #break based on current
            #when current goes to positive (?)
            #check if should be positive or negative based on reading the lines~10 into the cycle
            #save into dictorionary form and return
            #take out the capacity in this and save in another file
            #return as tuple, tuple
            for row in range(2, curSheet):
                curRow = curSheet[voltage + str(row)]
                nextRow = curSheet[capacity + str(row)]
                pass

    def plot_data(self, file_names, cycle_num, sheet_num, column_cell, 
                  graphTitle, AreaElectrode, 
                  YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
                  YaxisLabel,XaxisLabel):
        
        self.setParam(graphTitle, AreaElectrode, float(YAxisLimit), float(YAxisLower), 
                                            float(XAxisLimit), float(XAxisLower),YaxisLabel,XaxisLabel)     
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

            plt.plot(cycle_number,capacity)
 
            count +=1
                    
        
        #axis range
        plt.show()
        
    