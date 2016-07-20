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
var = testPlot.breakCycles(['Test.xlsx'], 'Record', 'A','E', 'I', 'F', 1.5)
pdb.set_trace()


print 'hello'
#     def plot_data(self, file_names, sheet_num, column_cell, set_num,
#                   graphTitle, AreaElectrode, 
#                   YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
#                   YaxisLabel,XaxisLabel

# testPlot.plot_data(['Test.xlsx'], 'sheetname1', 'B1', 1, 'Title', 1.5, 4,1,5,1,'dslfkj','sdlfkj')


