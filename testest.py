import pdb
import os
from openpyxl import load_workbook
import plotVoltage
from plotVoltage import PlotVoltage
import plotCapacity
from plotCapacity import PlotCapacity

#Test Plot Voltage
# wb = load_workbook('Test.xlsx')

# testPlot = PlotCapacity()

testPlot = PlotVoltage()
#    def breakCycles(self, filenames, sheetName, voltage, capacity, current, areaElectrode):
# var = testPlot.breakCycles(['Test.xlsx'], 'Record', 'A','E', 'I', 'F', 1.5)
# pdb.set_trace()
testPlot.plot_data(['Test.xlsx'], 1, 'Record', 'E', 'I', "graphTitle", 1, 'F', 'A', 20, 1, 20, 1, "YaxisLabel", "XaxisLabel")

# 
# 
#     def plot_data(self, file_names, cycle_num, sheet_num, VoltageCol, CapacityCol,
#                   graphTitle, AreaElectrode, 
#                   currentCol, cycleCol,
#                   YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, k
#                   YaxisLabel,XaxisLabel):

