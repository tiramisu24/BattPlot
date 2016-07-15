import os
import plotCapacity
from plotCapacity import PlotCapacity

#Test Plot Capacity
if False:
    print "hello"
else:
    print"hi"
testPlot = PlotCapacity()
# print os.getcwd()
# print testPlot.get_names(os.path.curdir)
# print testPlot.get_names(os.getcwd())
# new_path = "/Users/diane/Documents"
# print os.path.exists(new_path)
# os.chdir(new_path)
# print os.getcwd()

# test remove_names
# removeNames = ['createCell.py', 'PlotCapacity.py']
# print testPlot.remove_names(removeNames)
# print testPlot.remove_names(['fakename'])
# 
# test get_headings
# print testPlot.get_headings(['Test.xlsx'])

#test plot_data
testPlot.setParam("graphTitle", 1, 23, 1, 34, 5, 'YaxisLabel','XaxisLabel')
testPlot.plot_data(['Test.xlsx', 'Test Copy.xlsx'],'sheetname1', 'B1', 4, 
                                     'graphTitle', 1, 
                                    10, 1, 15, 2,
                                    'Capacity (mAh/cm2)','Cycle Number')


