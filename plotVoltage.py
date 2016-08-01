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
#         pdb.set_trace()
        wb = load_workbook(filename)
        
        curSheet = wb[sheetName]            
        max_length = curSheet.max_row                  
        prevCycle = 1
        
        for row in range(3, max_length+1):
            try:
                curCycle = int(curSheet[cycle + str(row)].value)
                curRowCur = curSheet[current + str(row)].value
                curRowCap = float(curSheet[capacity + str(row)].value)/float(self.areaElectrode)
                curRowVol = curSheet[voltage + str(row)].value
                prevRowVol = curSheet[voltage + str(row-1)].value
                #if change or if maxlength then append information?

                if row == max_length or curCycle>prevCycle:
#                     pdb.set_trace()

                    temp['chargeCap']=chargeCap
                    temp['chargeVol']=chargeVol
                    temp['dischargeCap']=discharCap
                    temp['dischargeVol']=discharVol

                    dictCycles[prevCycle]=temp                

                    chargeCap = []
                    chargeVol = []
                    discharCap = []
                    discharVol = []
                    temp ={}
                    
                    prevCycle = curCycle       
                
                if curRowCur ==0 or curRowCap ==0:
                    continue
    
                if prevRowVol<=curRowVol or curRowCur >0:
                    chargeCap.append(curRowCap)
                    chargeVol.append(curRowVol)
                    
                elif prevRowVol>=curRowVol or curRowCur <0:
                    discharCap.append(curRowCap)
                    discharVol.append(curRowVol)
            except:
                break
#         pdb.set_trace()
        return dictCycles

    def plot_data(self, file_names, graphTitle, AreaElectrode, numCycles,
                  currentCol, cycleCol,sheetName ,voltage, capacity,
                  YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
                  YaxisLabel,XaxisLabel):
        
        self.setParam(graphTitle, AreaElectrode, float(YAxisLimit), float(YAxisLower), 
                                            float(XAxisLimit), float(XAxisLower),YaxisLabel,XaxisLabel)     
        
#         pdb.set_trace()

        # add formating code
        for filename in file_names:
            comp = filename[-4:] 
            if (comp =='xlsx'):
#                     def breakCycles(self, filename, sheetName, cycle,voltage, capacity, current, areaElectrode):

                dictCycles = self.breakCycles(filename, sheetName ,cycleCol, voltage, capacity, currentCol, AreaElectrode)
            else:
                continue
#             pdb.set_trace()
            for cycle in numCycles:  
                cycle = int(cycle)                              
#               pdb.set_trace()
                tempDataList = dictCycles[cycle]
                line1, =plt.plot(tempDataList['chargeCap'],tempDataList['chargeVol'])
                line2, =plt.plot(tempDataList['dischargeCap'],tempDataList['dischargeVol'])            
                line1.set_label(str(cycle) + " Charge " + filename)
                line2.set_label(str(cycle) + " Discharge " + filename)
        
        #axis range
        plt.legend()
        plt.show()
        
    