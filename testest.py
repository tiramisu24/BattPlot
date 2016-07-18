import os
import plotVoltage
from plotVoltage import PlotVoltage
import pdb

#Test Plot Voltage
pdb.set_trace()

testPlot = PlotVoltage()
pdb.set_trace()
#    def breakCycles(self, filenames, sheetName, voltage, capacity, current, areaElectrode):
var = testPlot.breakCycles(['Text.xlsx'], 'Record', 'E1', 'I1', 'F1', 1.5)

#  plot_data(self, file_names, cycle_num, sheet_num, column_cell, 
#                   graphTitle, AreaElectrode, 
#                   YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
#                   YaxisLabel,XaxisLabel):

# testPlot.plot_data(['Test.xlsx'], 'sheetname1', 'B1', 1.5, 4)


