# -*- coding: utf-8 -*-

import fx
from fx import *
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
from tools.objectIterator import ObjectFinder
from tools.objectIterator import getObjects

try:
  _fromUtf8 = QtCore.QString.fromUtf8

except AttributeError:
  def _fromUtf8(s):
    return s
  
try:
  _encoding = QtWidgets.QApplication.UnicodeUTF8
  def _translate(context, text, disambig):
    return QtWidgets.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:
  def _translate(context, text, disambig):
    return QtWidgets.QApplication.translate(context, text, disambig)


class offset_dialog(QtWidgets.QWidget):
  def __init__(self, parent=None):
    QtWidgets.QWidget.__init__(self, parent)
    self.setWindowTitle("Offet All Keyframes")
    self.setObjectName(_fromUtf8("Dialog"))
    self.resize(200, 150)
    self.setMinimumSize(QtCore.QSize(200, 150))
    self.setMaximumSize(QtCore.QSize(200, 150))
    self.verticalLayout = QtWidgets.QVBoxLayout()
    self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
    self.horizontalLayout = QtWidgets.QHBoxLayout()
    self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
    self.old_firstframe_label = QtWidgets.QLabel()
    self.old_firstframe_label.setObjectName(_fromUtf8("old_firstframe_label"))
    self.horizontalLayout.addWidget(self.old_firstframe_label)
    self.old_firstframe_lineEdit = QtWidgets.QLineEdit()
    self.old_firstframe_lineEdit.setObjectName(_fromUtf8("old_firstframe_lineEdit"))
    self.horizontalLayout.addWidget(self.old_firstframe_lineEdit)
    self.verticalLayout.addLayout(self.horizontalLayout)
    self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
    self.new_firstframe_label = QtWidgets.QLabel()
    self.new_firstframe_label.setObjectName(_fromUtf8("new_firstframe_label"))
    self.horizontalLayout_2.addWidget(self.new_firstframe_label)
    self.new_firstframe_lineEdit = QtWidgets.QLineEdit()
    self.new_firstframe_lineEdit.setObjectName(_fromUtf8("new_firstframe_lineEdit"))
    self.horizontalLayout_2.addWidget(self.new_firstframe_lineEdit)
    self.verticalLayout.addLayout(self.horizontalLayout_2)
    self.buttonBox = QtWidgets.QDialogButtonBox()
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
    self.verticalLayout.addWidget(self.buttonBox)
    
    self.setLayout(self.verticalLayout)
    
    #Center the window
    frameGm = self.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft()) 
    
    self.old_firstframe_label.setText(_translate("Dialog", "Old First Frame:", None))
    self.new_firstframe_label.setText(_translate("Dialog", "New First Frame:", None))
    
    self.buttonBox.accepted.connect(self.beginOffsetprocess)
    self.buttonBox.rejected.connect(self.closeWindow)
    
    self.initialLoad()
    self.show()
    
    
    def initialLoad(self):
      self.getCurrentframe()
      
    def getCurrentframe(self):

      session = activeSession()
      
      currentframe = str(int(session.startFrame) + int(player.frame))
      self.old_firstframe_lineEdit.setText(currentframe)
    
    def beginOffsetprocess(self):
      
      oldfirstframe = int(self.old_firstframe_lineEdit.text())
      newfirstframe = int(self.new_firstframe_lineEdit.text())
      
      offset = int(newfirstframe - oldfirstframe)
      
      node = activeNode()
      
      if node:
        finder = ObjectFinder(hidden = True)
        objects = finder.find(node.children)
        
        beginUndo("Offset Keyframes")
        
        for object in objects:
          for prop in object.properties:
            if object.property(prop).keyframable:
              object.property(prop).moveKeys(offset)
        
        endUndo()
        
        self.closeWindow()
        
    def closeWindow(self):
      self.close()



class offsetAllKeyframes(fx.Action):  
  def __init__(self):
    fx.Action.__init__(self, 'EM Time | Offset All Keyframes')
  
  def execute(self):
    global win
    win = offset_dialog()

fx.addAction(offsetAllKeyframes())