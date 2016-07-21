import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from plotCapacity import *
import pdb
from plotVoltage import PlotVoltage

class tabdemo(QTabWidget):
    capacityGraph = PlotCapacity()
    voltageGraph = PlotVoltage()
    path_names=[]
    dict_path_names={}
    list_names = []
    list_checkboxes=[]
    headings=[]
    sheetnames = []
    capacity_cell=''
    sheetName = 'Sheet'
    setNum = 4
#     cycleDict = {}
    areaElectrode=1
#     cycleCol=''
#     voltageCol=''
#     currentCol=''


    
    def __init__(self, parent = None):
        super(tabdemo, self).__init__(parent)
        self.listWidget = QtGui.QListWidget()
        
        self.tab0 = QWidget() 
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        
        self.resize(800,800)
        
        self.addTab(self.tab0,"Tab 0")
        self.addTab(self.tab1,"Tab 1")
        self.addTab(self.tab2, "Tab 2")

        
        self.tab0UI()
        self.tab1UI()
        self.tab2UI()

        self.setWindowTitle("Battery")
        
    
    def tab0UI(self):
        
        layout = QFormLayout()
        bt = QPushButton()
        layout.addRow("Import",bt) 
        fList = QComboBox()     
        layout.addRow("List",fList)
        bt.clicked.connect(self.loadFile) 
        bt.clicked.connect(lambda: self.populateChecklist(self.tab1.filenameBox,self.dict_path_names))
#                 self.populateChecklist(self.tab1.filenameBox,self.dict_path_names)
    
        self.setTabText(0,"Import")
        self.tab0.setLayout(layout)
        
        #let them do selection?

    def loadFile(self):    
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '\home')
         
        for item in fname:
            f = open(item, 'r')
            ss = f.name
            self.path_names.append(ss)
            ss_split = ss.split('/')
            self.dict_path_names[ss_split[-1]]= ss
            self.tab0.children()[4].addItem(ss)
            self.show()
#         pdb.set_trace()
#     def populateChecklist(self):      
#         row = 0
#         for eachName in self.dict_path_names:
#             newCheckBox = QtGui.QTableWidgetItem(eachName)
#             newCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
#             newCheckBox.setCheckState(QtCore.Qt.Unchecked)
#             
#             self.tab1.filenameBox.insertRow(row)
#             self.tab1.filenameBox.setItem(row, 1 , newCheckBox)
# 
#         row +=1        
#           
#         self.tab1.filenameBox.itemClicked.connect(self.clicked)


    def populateChecklist(self,Box, thisList):      
        row = 0
#         pdb.set_trace()
        for eachName in thisList:
            newCheckBox = QtGui.QTableWidgetItem(eachName)
            newCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
            newCheckBox.setCheckState(QtCore.Qt.Unchecked)
            
            Box.insertRow(row)
            Box.setItem(row, 1 , newCheckBox)

        row +=1        
          
        Box.itemClicked.connect(self.clicked)

    def clicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.addName(item.text())
        else:
            self.removeName(item.text())
 


    def removeName(self, name):
        path_name = self.dict_path_names[name]
        try:
            self.list_names.remove(str(path_name))
        except ValueError:
            pass
        self.list_names.sort()
    
    def addName(self,name):
        path_name = self.dict_path_names[name]
        self.list_names.append(str(path_name))
        self.list_names.sort()
                    
          
    def tab1UI(self):
        #populate entry fields and save information
        layout = QVBoxLayout()       
        layoutTop = QHBoxLayout()
        selectionLayout = QVBoxLayout()
        
        self.tab1.filenameBox = QTableWidget(1,1)
        self.tab1.optionBox = QVBoxLayout()

        
        formLayout = QFormLayout()
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        radioBoxLayout = QHBoxLayout()
        

        bt1 = QPushButton()
        bt1.toggle()
        bt1.setText("Plot")
        bt1.resize(5,10)
        bt2 = QPushButton()
        bt2.toggle()
        bt2.setText("Okay")
        bt2.resize(5,10)
        self.tab1.rbt = QRadioButton('Set')
        self.tab1.rbt2 = QRadioButton('Custom')
        
        
        
        graphTitle = QLineEdit()        
        AreaElectrode = QLineEdit()
        YAxisLimit = QLineEdit()
        YAxisLower = QLineEdit()
        XAxisLimit = QLineEdit()
        XAxisLower = QLineEdit()
        Sheet = QComboBox()
        Column = QComboBox()
        
        radioBoxLayout.addWidget(self.tab1.rbt)
        radioBoxLayout.addWidget(self.tab1.rbt2)
        formLayout.addRow("Sheet Name",Sheet)
        formLayout.addRow("Column",Column)
       
        formLayout.addRow("Name",graphTitle)
        formLayout.addRow("Area",AreaElectrode)
        
        #add checkbox for auto axis
        formLayout.addRow("YAxis limit", YAxisLimit)
        formLayout.addRow("YAxis lower", YAxisLower)
        formLayout.addRow("XAxis limit", XAxisLimit)
        formLayout.addRow("XAxis limit", XAxisLower)        
        formLayout.addRow("Num in Set", radioBoxLayout)
        formLayout.addRow(self.tab1.optionBox)
        
        selectionLayout.addWidget(self.tab1.filenameBox)
        
        #formattings
        selectionLayout.addWidget(bt2)
        hbox.addWidget(bt1)
        vbox.addWidget(bt1)
                
        vbox.addLayout(hbox)
        layoutTop.addLayout(selectionLayout)
        layoutTop.addLayout(formLayout)
#         layoutTop.addLayout(self.tab1.optionBox)

 
        layout.addLayout(layoutTop)
        layout.addLayout(vbox)

        layout.addWidget(bt2)
        
        self.areaElectrode=AreaElectrode.text()
        bt1.clicked.connect(lambda: self.plotCapGraph(graphTitle.text(), AreaElectrode.text(), YAxisLimit.text(),
                                                     YAxisLower.text(), XAxisLimit.text(), XAxisLower.text()))

        bt2.clicked.connect(self.setSheetName)
        bt2.clicked.connect(self.setCycleName)
            
        self.tab1.rbt.clicked.connect(self.autoSet)
        self.tab1.rbt2.clicked.connect(self.customSet)
        
        Sheet.activated.connect(self.getSheet)

        Sheet.activated.connect(self.setHeadings)

        Column.activated[str].connect(self.getColumn)
        
        self.setTabText(1,"Cycling")
        self.tab1.setLayout(layout)
    
    def autoSet(self):
        if self.tab1.optionBox.isEmpty() == False:
            try:
                self.tab1.optionBox.removeWidget(self.tab1.setCustom)
            except:
                pass
            
        if self.tab1.optionBox.isEmpty():
            setOptions = range(1,9)
            self.tab1.setComboBox = QComboBox()
            for num in setOptions:
                self.tab1.setComboBox.addItems(str(num))

            self.tab1.optionBox.addWidget(self.tab1.setComboBox) 
            self.tab1.setComboBox.activated[str].connect(self.setGroupNum)
                
    def customSet(self):
#         pdb.set_trace()
            
        if self.tab1.optionBox.isEmpty() == False:
            try:
                self.tab1.optionBox.removeWidget(self.tab1.setComboBox)
            except AttributeError:
                pass

            
        if self.tab1.optionBox.isEmpty():
            self.tab1.setCustom = QLineEdit()
            self.tab1.optionBox.addWidget(self.tab1.setCustom)

    def setGroupNum(self, num):
        self.setNum = int(num)
    
    def setAxis(self,YAxisLimit, YAxisLower, XAxisLimit, XAxisLower):
        try:
            XAxisLimit= float(XAxisLimit)           
        except ValueError:            
            XAxisLimit = 50           
        try:
            XAxisLower = float(XAxisLower) 
        except ValueError:
            XAxisLower =0
        try: 
            YAxisLimit = float(YAxisLimit)
        except ValueError:
            YAxisLimit = 6
        try:
            YAxisLower = float(YAxisLower)
        except ValueError:
            YAxisLower = 0
        
        return [YAxisLimit, YAxisLower, XAxisLimit, XAxisLower]

    def plotCapGraph(self, graphTitle, AreaElectrode, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower):
        axisRange = self.setAxis(YAxisLimit, YAxisLower, XAxisLimit, XAxisLower)
#         pdb.set_trace()

#         self.setGroupNum(self.tab1.setCustom.text())  

        self.capacityGraph.plot_data(self.list_names, self.sheetName, self.capacity_cell, self.setNum, 
                                                 graphTitle, AreaElectrode, 
                                                 axisRange[0], axisRange[1], axisRange[2], axisRange[3],
                                                'Capacity (mAh/cm2)','Cycle Number')
    
    #make this more general!!
    def populateComboBox(self, box, thisList):
        box.clear()
        for item in thisList:
            box.addItem(str(item))
            self.show()
            
        box.setCurrentIndex(0)
    
    def setHeadings(self):
        self.headings = self.capacityGraph.get_headings(self.list_names,self.sheetName)
        headingTitle= self.headings.keys()
        self.tab1.children()[6].clear()

        for headingName in headingTitle:
            self.tab1.children()[6].addItem(str(headingName))
            self.show()
        self.tab1.children()[6].setCurrentIndex(0)

    def setSheetName(self):
        self.sheetnames = self.capacityGraph.get_sheetnames(self.list_names)
        self.tab1.children()[4].clear()
        for sheet in self.sheetnames:
            self.tab1.children()[4].addItem(sheet)
            self.show()
        
        self.tab1.children()[4].setCurrentIndex(0)
        self.getSheet(0)
        self.setHeadings()

    def setCycleName(self, cycle, voltage,current):
        cycleDict = self.voltageGraph.breakCycles(self.list_names, self.sheetName, cycle, voltage, 
                                                       self.capacity_cell, current, self.areaElectrode)
        #set this as break cycles?
        return cycleDict
        pass
    def getColumn(self, dictKey):
        self.capacity_cell = self.headings[str(dictKey)]
        self.capacity_cell = self.capacity_cell[0]
    
    def getSheet(self, selectSheetIndex):
        self.sheetName = self.sheetnames[selectSheetIndex]
        
    def tab2UI(self):
         #populate entry fields and save information
        layout = QVBoxLayout()       
        layoutTop = QHBoxLayout()
        selectionLayout = QVBoxLayout()
        
        self.tab2.cycleNumberBox = QTableWidget(1,1)
        
        formLayout = QFormLayout()
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        

        bt1 = QPushButton()
        bt1.toggle()
        bt1.setText("Plot")
        bt1.resize(5,10)
        okButton = QPushButton()
        okButton.toggle()
        okButton.setText("Okay")
        okButton.resize(5,10)
        
        graphTitle = QLineEdit()        
        YAxisLimit = QLineEdit()
        YAxisLower = QLineEdit()
        XAxisLimit = QLineEdit()
        XAxisLower = QLineEdit()
        #change the next 3 to combobox
        
        Cycle = QComboBox()
        Voltage = QComboBox()
        Current = QComboBox()

       
        formLayout.addRow("Name",graphTitle)
        #add checkbox for auto axis
        formLayout.addRow("YAxis limit", YAxisLimit)
        formLayout.addRow("YAxis lower", YAxisLower)
        formLayout.addRow("XAxis limit", XAxisLimit)
        formLayout.addRow("XAxis limit", XAxisLower)
        formLayout.addRow("Cycle", Cycle)
        formLayout.addRow("Voltage", Voltage)
        formLayout.addRow("Current", Current)
        
        selectionLayout.addWidget(self.tab2.cycleNumberBox)

        okButton.clicked.connect(lambda: self.setCycleName(Cycle.text(), Voltage.text(), Current.text()))

        
        bt1.clicked.connect(lambda: self.graphVoltage(graphTitle.text(), YAxisLimit.text(),
                                             YAxisLower.text(), XAxisLimit.text(), XAxisLower.text()))

        
        #formattings
        hbox.addWidget(okButton)
        vbox.addWidget(okButton) 
        hbox.addWidget(bt1)
        vbox.addWidget(bt1)
               
                
        vbox.addLayout(hbox)
        layoutTop.addLayout(selectionLayout)
        layoutTop.addLayout(formLayout)
 
        layout.addLayout(layoutTop)
        layout.addLayout(vbox)
        
        self.setTabText(2,"Voltage Curves")
        self.tab2.setLayout(layout)

    def graphVoltage(self, graphTitle, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower):
        axisRange = self.setAxis(YAxisLimit, YAxisLower, XAxisLimit, XAxisLower)

        

#         self.voltageGraph.plot_data(self.list_names, cycle_num, self.sheetName, VoltageCol, CapacityCol, graphTitle, AreaElectrode, currentCol, cycleCol, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, YaxisLabel, XaxisLabel)
#         self.voltageGraph.plot_data(self.list_names, cycle_num, self.sheetName, VoltageCol, CapacityCol, graphTitle, AreaElectrode, currentCol, cycleCol, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, YaxisLabel, XaxisLabel)


#    def plot_data(self, file_names, cycle_num, sheet_num, VoltageCol, CapacityCol,
#                   graphTitle, AreaElectrode, 
#                   currentCol, cycleCol,
#                   YAxisLimit, YAxisLower, XAxisLimit, XAxisLower, 
#                   YaxisLabel,XaxisLabel):
#             
        
def main():
    app = QApplication(sys.argv)
    ex = tabdemo()
    ex.show()
    sys.exit(app.exec_())
 
   
if __name__ == '__main__':
    main()
