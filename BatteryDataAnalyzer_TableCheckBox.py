import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from plotCapacity import *
import pdb
from plotVoltage import *

class tabdemo(QTabWidget):
    capacityGraph = PlotCapacity()
    voltageGraph = PlotVoltage()
    path_names=[]
    dict_path_names={}
    list_names = []
    headingsCapacity=[]
    sheetnames = []
    capacity_cell=''
    capacityCellV=''
    cycleCell =''
    voltageCell = ''
    currentCell = ''
    sheetNameCapacity = 'Sheet'
    setNum = 4
    areaElectrode=1
    listCycles = []
    listCyclesAllKeys ={}
    voltageData = {}
  
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
        self.setTabText(0,"Import")
        self.tab0.setLayout(layout)
        
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
        print "remove"
        self.list_names.sort()
    
    def addName(self,name):
        path_name = self.dict_path_names[name]
        self.list_names.append(str(path_name))
        print "add"
        self.list_names.sort()
        
                    
          
    def tab1UI(self):
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
        

        plotBotton = QPushButton()
        plotBotton.toggle()
        plotBotton.setText("Plot")
        plotBotton.resize(5,10)
        okButton = QPushButton()
        okButton.toggle()
        okButton.setText("Okay")
        okButton.resize(5,10)
        clearButton = QPushButton()
        clearButton.toggle()
        clearButton.setText('Clear Cache')
        clearButton.resize(5,10)
        self.tab1.rbt = QRadioButton('Set')
        self.tab1.rbt2 = QRadioButton('Custom')
        
        graphTitle = QLineEdit()        
        self.tab1.AreaElectrode = QLineEdit()
        YAxisLimit = QLineEdit()
        YAxisLower = QLineEdit()
        XAxisLimit = QLineEdit()
        XAxisLower = QLineEdit()
        self.tab1.Sheet = QComboBox()
        self.tab1.Column = QComboBox()
        
        radioBoxLayout.addWidget(self.tab1.rbt)
        radioBoxLayout.addWidget(self.tab1.rbt2)
        formLayout.addRow("Sheet Name",self.tab1.Sheet)
        formLayout.addRow("Column",self.tab1.Column)
       
        formLayout.addRow("Name",graphTitle)
        formLayout.addRow("Area",self.tab1.AreaElectrode)
        
        formLayout.addRow("YAxis limit", YAxisLimit)
        formLayout.addRow("YAxis lower", YAxisLower)
        formLayout.addRow("XAxis limit", XAxisLimit)
        formLayout.addRow("XAxis limit", XAxisLower)        
        formLayout.addRow("Num in Set", radioBoxLayout)
        formLayout.addRow(self.tab1.optionBox)
        
        selectionLayout.addWidget(self.tab1.filenameBox)
        
        selectionLayout.addWidget(okButton)
        selectionLayout.addWidget(clearButton)
        hbox.addWidget(plotBotton)
        vbox.addWidget(plotBotton)
                
        vbox.addLayout(hbox)
        layoutTop.addLayout(selectionLayout)
        layoutTop.addLayout(formLayout)

 
        layout.addLayout(layoutTop)
        layout.addLayout(vbox)

        layout.addWidget(okButton)
        layout.addWidget(clearButton)
        

        plotBotton.clicked.connect(lambda: self.plotCapGraph(graphTitle.text(), YAxisLimit.text(),
                                                     YAxisLower.text(), XAxisLimit.text(), XAxisLower.text()))

        okButton.clicked.connect(self.setSheetName)
        okButton.clicked.connect(self.setSheetNameVoltage)
        clearButton.clicked.connect(self.clearTable)
            
        self.tab1.rbt.clicked.connect(self.autoSet)
        self.tab1.rbt2.clicked.connect(self.customSet)
        
        self.tab1.Sheet.activated.connect(self.getSheet)


        self.tab1.Column.activated[str].connect(self.getColumn)
        
        self.setTabText(1,"Cycling")
        self.tab1.setLayout(layout)
    
    def clearTable(self):
        self.list_names=[]
        self.listCycles = []

    
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
            YAxisLimit = float(YAxisLimit)
        except ValueError:
            YAxisLimit = 6
        try:
            YAxisLower = float(YAxisLower)
        except ValueError:
            YAxisLower = 0
        try:
            XAxisLimit= float(XAxisLimit)           
        except ValueError:            
            XAxisLimit = 50           
        try:
            XAxisLower = float(XAxisLower) 
        except ValueError:
            XAxisLower =0        
        return [YAxisLimit, YAxisLower, XAxisLimit, XAxisLower]

    def plotCapGraph(self, graphTitle, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower):
        axisRange = self.setAxis(YAxisLimit, YAxisLower, XAxisLimit, XAxisLower)
        self.areaElectrode=self.tab1.AreaElectrode.text()

        self.capacityGraph.plot_data(self.list_names, self.sheetName, self.capacity_cell, self.setNum, 
                                                 graphTitle, self.areaElectrode, 
                                                 axisRange[0], axisRange[1], axisRange[2], axisRange[3],
                                                'Capacity (mAh/cm2)','Cycle Number')
    
    def populateComboBox(self, box, thisList):
        box.clear()
        for item in thisList:
            box.addItem(str(item))
            self.show()            
        box.setCurrentIndex(0)
    

        
    def setSheetName(self):
        self.sheetnames = self.capacityGraph.get_sheetnames(self.list_names)
        self.populateComboBox(self.tab1.Sheet, self.sheetnames)
        
    def setSheetNameVoltage(self):
        self.sheetnames = self.voltageGraph.get_sheetnames(self.list_names)
        self.populateComboBox(self.tab2.Sheet, self.sheetnames)
            
    def setHeadings(self):
        self.headingsCapacity = self.capacityGraph.get_headings(self.list_names, self.sheetName)
        headingTitle= self.headingsCapacity.keys()
        self.populateComboBox(self.tab1.Column, headingTitle)

    def setHeadingsVoltage(self):
        self.headingsCapacity = self.capacityGraph.get_headings(self.list_names, self.sheetName)
        headingTitle= self.headingsCapacity.keys()
        self.populateComboBox(self.tab2.Cycle, headingTitle) 
        self.populateComboBox(self.tab2.Voltage, headingTitle) 
        self.populateComboBox(self.tab2.Current, headingTitle) 
        self.populateComboBox(self.tab2.CapacityV, headingTitle) 

    def setCycleName(self, cycle, voltage,current, capacity):

        for filename in self.list_names:
            comp = filename[-4:] 
            if (comp =='xlsx'):
                ########
                #write function to find the cell with least cycles
                ########
                self.voltageData = self.voltageGraph.breakCycles(filename, self.sheetName, cycle, voltage, 
                                                       capacity, current, self.areaElectrode)
                break
            else:
                continue
            
        self.listCyclesAllKeys = self.voltageData.keys()
        self.populateChecklistDict(self.tab2.cycleNumberBox, self.listCyclesAllKeys)

        
    def populateChecklist(self,Box, thisList):      
        row = 0
        pdb.set_trace()
        thisList=sorted(thisList)
        for eachName in thisList:
            newCheckBox = QtGui.QTableWidgetItem(str(eachName))
            newCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
            newCheckBox.setCheckState(QtCore.Qt.Unchecked)
            
            Box.insertRow(row)
            Box.setItem(row, 1 , newCheckBox)
        Box.itemClicked.connect(self.clicked)       
            
        
    def populateChecklistDict(self,Box, thisDict):  
        row = 0
        for eachName in thisDict:
            newCheckBox = QtGui.QTableWidgetItem(str(eachName))
            newCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
            newCheckBox.setCheckState(QtCore.Qt.Unchecked)
            
            Box.insertRow(row)
            Box.setItem(row, 1 , newCheckBox)

        Box.itemClicked.connect(self.clickedV)  
        
    def clickedV(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.addNameV(item.text())
        else:
            self.removeNameV(item.text())

    def removeNameV(self, name):
        try:
            self.listCycles.remove(str(name))
        except ValueError:
            pass
        
        self.listCycles.sort()
    
    def addNameV(self,name):
        self.listCycles.append(str(name))
        self.listCycles.sort()  
      
        
    def getColumn(self, dictKey):
        self.capacity_cell = self.headingsCapacity[str(dictKey)]
        self.capacity_cell = self.capacity_cell[0]
   
    def getColumnCycle(self, dictKey):
        self.cycleCell = self.headingsCapacity[str(dictKey)]
        self.cycleCell = self.cycleCell[0]
    
    def getColumnVoltage(self, dictKey):
        self.voltageCell = self.headingsCapacity[str(dictKey)]
        self.voltageCell = self.voltageCell[0]
    
    def getColumnCapacity(self, dictKey):
        self.capacityCellV = self.headingsCapacity[str(dictKey)]
        self.capacityCellV = self.capacityCellV[0]
    
    def getColumnCurrent(self, dictKey):
        self.currentCell = self.headingsCapacity[str(dictKey)]
        self.currentCell = self.currentCell[0]
    
    def getSheet(self, selectSheetIndex):
        self.sheetName = self.sheetnames[selectSheetIndex]
        self.setHeadings()
        
    def getSheetVoltage(self, selectSheetIndex):
        self.sheetName = self.sheetnames[selectSheetIndex]
        self.setHeadingsVoltage()

        
    def tab2UI(self):
        layout = QVBoxLayout()       
        layoutTop = QHBoxLayout()
        selectionLayout = QVBoxLayout()
        
        self.tab2.cycleNumberBox = QTableWidget(1,1)
        
        formLayout = QFormLayout()
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        

        plotButton = QPushButton()
        plotButton.toggle()
        plotButton.setText("Plot")
        plotButton.resize(5,10)
        okButton = QPushButton()
        okButton.toggle()
        okButton.setText("Okay")
        okButton.resize(5,10)
        
        graphTitle = QLineEdit()        
        YAxisLimit = QLineEdit()
        YAxisLower = QLineEdit()
        XAxisLimit = QLineEdit()
        XAxisLower = QLineEdit()
        self.tab2.Sheet = QComboBox()
        self.tab2.Cycle = QComboBox()
        self.tab2.Voltage = QComboBox()
        self.tab2.Current = QComboBox()
        self.tab2.CapacityV = QComboBox()


       
        formLayout.addRow("Name",graphTitle)
        formLayout.addRow("YAxis limit", YAxisLimit)
        formLayout.addRow("YAxis lower", YAxisLower)
        formLayout.addRow("XAxis limit", XAxisLimit)
        formLayout.addRow("XAxis limit", XAxisLower)
        formLayout.addRow("Sheetname", self.tab2.Sheet)        
        formLayout.addRow("Cycle", self.tab2.Cycle)
        formLayout.addRow("Voltage", self.tab2.Voltage)
        formLayout.addRow("Current", self.tab2.Current)
        formLayout.addRow("Capacity", self.tab2.CapacityV)

        
        selectionLayout.addWidget(self.tab2.cycleNumberBox)

        hbox.addWidget(okButton)
        vbox.addWidget(okButton) 
        hbox.addWidget(plotButton)
        vbox.addWidget(plotButton)
               
                
        vbox.addLayout(hbox)
        layoutTop.addLayout(selectionLayout)
        layoutTop.addLayout(formLayout)
 
        layout.addLayout(layoutTop)
        layout.addLayout(vbox)
        
        self.setTabText(2,"Voltage Curves")
        self.tab2.setLayout(layout)
        self.tab2.Cycle.activated[str].connect(self.getColumnCycle)
        self.tab2.Voltage.activated[str].connect(self.getColumnVoltage)
        self.tab2.Current.activated[str].connect(self.getColumnCurrent)
        self.tab2.CapacityV.activated[str].connect(self.getColumnCapacity)        
        
        self.tab2.Sheet.activated.connect(self.getSheetVoltage)
        okButton.clicked.connect(lambda: self.setCycleName(self.cycleCell, self.voltageCell,self.currentCell, self.capacityCellV))
        plotButton.clicked.connect(lambda: self.graphVoltage(graphTitle.text(), YAxisLimit.text(), YAxisLower.text(), XAxisLimit.text(), XAxisLower.text()))
    
    
    def graphVoltage(self, graphTitle, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower):
        self.areaElectrode=self.tab1.AreaElectrode.text()

        axisRange = self.setAxis(YAxisLimit, YAxisLower, XAxisLimit, XAxisLower)   
  
        self.voltageGraph.plot_data(self.list_names, graphTitle, self.areaElectrode, self.listCycles,
                                    self.currentCell, self.cycleCell, self.sheetName, self.voltageCell, self.capacityCellV,
                                    axisRange[0], axisRange[1], axisRange[2], axisRange[3], 
                                    'Voltage', 'Capacity ')
        
def main():
    app = QApplication(sys.argv)
    ex = tabdemo()
    ex.show()
    sys.exit(app.exec_())
 
   
if __name__ == '__main__':
    main()
