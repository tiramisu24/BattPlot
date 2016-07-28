import openpyxl
import os
import plotGraph
from plotGraph import PlotGraph
from os import listdir
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import pdb

class PlotVoltage(PlotGraph):
    areaElectrode =1
        
    def breakCycles(self, filename, sheetName, cycle,voltage, capacity, current, areaElectrode):
        #voltage and capacity returns column names
        #returns inidividual cycles of filenames selected
        dictCycles ={}

        temp = {}
        chargeCap = []
        chargeVol = []
        discharCap = []
        discharVol = []
        pdb.set_trace()
        wb = load_workbook(filename)
        
        curSheet = wb[sheetName]            
        max_length = curSheet.max_row                  
        prevCycle = 1
        
        for row in range(3, max_length+1):
            try:
#                 pdb.set_trace()
                curCycle = int(curSheet[cycle + str(row)].value)
                curRowCur = curSheet[current + str(row)].value
                curRowCap = float(curSheet[capacity + str(row)].value)/float(self.areaElectrode)
                curRowVol = curSheet[voltage + str(row)].value
                prevRowVol = curSheet[voltage + str(row-1)].value
                #if change or if maxlength then append information?
                if row == max_length or curCycle>prevCycle: # or bigger than the next
                    temp['chargeCap']=chargeCap
                    temp['chargeVol']=chargeVol
                    temp['dischargeCap']=discharCap
                    temp['dischargeVol']=discharVol
                 
                    dictCycles[prevCycle]=temp                
                    prevCycle = curCycle       
                
                if curRowCur ==0:
                    continue
    
                if prevRowVol<=curRowVol or curRowCur >0:
                    chargeCap.append(curRowCap)
                    chargeVol.append(curRowVol)
                    
                elif prevRowVol>=curRowVol or curRowCur <0:
                    discharCap.append(curRowCap)
                    discharVol.append(curRowVol)
            except:
                break
        pdb.set_trace()
        return dictCycles

    def plot_data(self, file_names, dictCycles,
                  graphTitle, AreaElectrode, 
                  currentCol, cycleCol,
                  YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
                  YaxisLabel,XaxisLabel):
        
        self.setParam(graphTitle, AreaElectrode, float(YAxisLimit), float(YAxisLower), 
                                            float(XAxisLimit), float(XAxisLower),YaxisLabel,XaxisLabel)     
        
#         pdb.set_trace()

        # add formating code
        cycleNum = dictCycles.keys()
        
        for file_name in file_names:

            
            for num in cycleNum:                
#                 pdb.set_trace()

                tempDataList = dictCycles[num]
                line1, =plt.plot(tempDataList['chargeCap'],tempDataList['chargeVol'])
                line2, =plt.plot(tempDataList['dischargeCap'],tempDataList['dischargeVol'])
            
                line1.set_label(num)
                line2.set_label(num)
        
        #axis range
        plt.legend()
        plt.show()
        
    