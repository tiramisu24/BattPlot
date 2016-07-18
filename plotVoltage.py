import openpyxl
import os
import plotGraph
from plotGraph import PlotGraph
from os import listdir
from openpyxl import load_workbook
import matplotlib.pyplot as plt

class PlotVoltage(plotGraph):
        
    def breakCycles(self, filenames, sheetName, voltage, capacity, current, areaElectrode):
        #voltage and capacity returns column names
        #returns inidividual cycles of filenames selected
        dictCycles ={}

        num = 1
        for eachFile in filenames:
            temp = {}
            chargeCap = []
            chargeVol = []
            discharCap = []
            discharVol = []
            comp = eachFile[-4:] 
            if (comp =='xlsx'):
                wb = load_workbook(eachFile, data_only= True)
            else:
                continue
            
            curSheet = wb[sheetName]
                        
            
            for row in range(2, curSheet):
                curRowCur = curSheet[current + str(row)]
                curRowCap = float(curSheet[capacity + str(row)])/float(areaElectrode)
                curRowVol = curSheet[voltage + str(row)]
                nextRowVol = curSheet[voltage + str(row)]
                
                if nextRowVol>=curRowVol or curRowCur >0:
                    chargeCap.append(curRowCap)
                    chargeVol.append(curRowVol)
                    
                elif nextRowVol<=curRowVol or curRowCur <0:
                    discharCap.append(curRowCap)
                    discharVol.append(curRowVol)
            
            temp['chargeCap']=chargeCap
            temp['chargeVol']=chargeVol
            temp['dischargeCap']=discharCap
            temp['dischargeVol']=discharVol
            
            dictCycles[str(num)]=temp
            num +=1
        #returns a dictionary of dictionaries    
        return dictCycles

    def plot_data(self, file_names, cycle_num, sheet_num, VoltageCol, CapacityCol,
                  graphTitle, AreaElectrode, 
                  YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
                  YaxisLabel,XaxisLabel):
        
        self.setParam(graphTitle, AreaElectrode, float(YAxisLimit), float(YAxisLower), 
                                            float(XAxisLimit), float(XAxisLower),YaxisLabel,XaxisLabel)     
        
        
        #call break cycle         
        count =0
        column_name = VoltageCol[0]
        # add formating code
        for file_name in file_names:
            count +=1
                    
        
        #axis range
        plt.show()
        
    