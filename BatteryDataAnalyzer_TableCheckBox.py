import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from plotCapacity import *
import pdb

class tabdemo(QTabWidget):
    capacityGraph = PlotCapacity()
    path_names=[]
    dict_path_names={}
    list_names = []
    list_checkboxes=[]
    headings=[]
    sheetnames = []
    column_cell=''
    sheetName = 'Sheet'
    setNum = 4


    
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
        self.populateChecklist()

    def populateChecklist(self):      
        row = 0
        for eachName in self.dict_path_names:
            newCheckBox = QtGui.QTableWidgetItem(eachName)
            newCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable |QtCore.Qt.ItemIsEnabled)
            newCheckBox.setCheckState(QtCore.Qt.Unchecked)
            
            self.tab1.filenameBox.insertRow(row)
            self.tab1.filenameBox.setItem(row, 1 , newCheckBox)

        row +=1        
          
        self.tab1.filenameBox.itemClicked.connect(self.clicked)

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
        bt2.setText("Ok")
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
        
        bt1.clicked.connect(lambda: self.plotGraph(graphTitle.text(), AreaElectrode.text(), YAxisLimit.text(),
                                                     YAxisLower.text(), XAxisLimit.text(), XAxisLower.text()))

        bt2.clicked.connect(self.setSheetName)
            
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

#             self.setGroupNum(self.tab1.setCustom.text())  
    
    
    def setGroupNum(self, num):
        self.setNum = int(num)


    def plotGraph(self, graphTitle, AreaElectrode, YAxisLimit, YAxisLower, XAxisLimit, XAxisLower):
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
#         pdb.set_trace()

#         self.setGroupNum(self.tab1.setCustom.text())  

        self.capacityGraph.plot_data(self.list_names, self.sheetName, self.column_cell, self.setNum, 
                                                 graphTitle, AreaElectrode, 
                                                XAxisLimit, XAxisLower,  YAxisLimit, YAxisLower, 
                                                'Capacity (mAh/cm2)','Cycle Number')

    
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


    def getColumn(self, dictKey):
        self.column_cell = self.headings[str(dictKey)]
    
    def getSheet(self, selectSheetIndex):
        self.sheetName = self.sheetnames[selectSheetIndex]
        
    def tab2UI(self):
         #populate entry fields and save information
        layout = QVBoxLayout()       
        layoutTop = QHBoxLayout()
        selectionLayout = QVBoxLayout()
        
        self.tab2.filenameBox = QTableWidget(1,1)
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
        
        graphTitle = QLineEdit()        
        YAxisLimit = QLineEdit()
        YAxisLower = QLineEdit()
        XAxisLimit = QLineEdit()
        XAxisLower = QLineEdit()

       
        formLayout.addRow("Name",graphTitle)
        #add checkbox for auto axis
        formLayout.addRow("YAxis limit", YAxisLimit)
        formLayout.addRow("YAxis lower", YAxisLower)
        formLayout.addRow("XAxis limit", XAxisLimit)
        formLayout.addRow("XAxis limit", XAxisLower)
        
        selectionLayout.addWidget(self.tab2.filenameBox)
        selectionLayout.addWidget(self.tab2.cycleNumberBox)

        bt1.clicked.connect(lambda: self.plotVoltage(graphTitle.text(), YAxisLimit.text(),
                                             YAxisLower.text(), XAxisLimit.text(), XAxisLower.text()))

        
        #formattings
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

#new class called plotVoltage?        
#         self.capacityGraph.plot_data(self.list_names, 'sheetname1', self.column_cell, 4, 
#                                             graphTitle,
#                                             XAxisLimit, XAxisLower,  YAxisLimit, YAxisLower, 
#                                             'Capacity (mAh/cm2)','Cycle Number')
# 
#             
        
def main():
    app = QApplication(sys.argv)
    ex = tabdemo()
    ex.show()
    sys.exit(app.exec_())
 
   
if __name__ == '__main__':
    main()
