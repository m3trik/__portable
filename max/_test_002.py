from PySide2 import QtGui, QtCore, QtWidgets

import os.path, sys


# class PopupDialogMixin(object):  # will not work (with PySide at least) unless implemented as 'new style' class. I.e inherit from object
# 	def makePopup(callWidget):
# 		"""
# 		Turns the dialog into a popup dialog.
# 		callWidget is the widget responsible for calling the dialog (e.g. a toolbar button)
# 		"""
# 		self.setContentsMargins(0,0,0,0)
# 		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
# 		self.setObjectName('ImportDialog')

# 		# Move the dialog to the widget that called it
# 		point = callWidget.rect().bottomRight()
# 		global_point = callWidget.mapToGlobal(point)
# 		self.move(global_point - QtCore.QPoint(self.width(), 0))



# #Your custom dialog would then inherit from both QtCore.QDialog and PopupDialogMixin. 
# #This gives you the option to use your dialog in the 'normal' way or make it a popup dialog. e.g:
# dlg = MyDialog(self)
# dlg.makePopup(self.myButton)

class popup(QtWidgets.QWidget):
	def __init__(self, parent = None, widget=None):    
		QtWidgets.QWidget.__init__(self, parent)
		layout = QtWidgets.QGridLayout(self)
		button = QtWidgets.QPushButton("Popup")
		layout.addWidget(button)

		# adjust the margins or you will get an invisible, unintended border
		layout.setContentsMargins(0, 0, 0, 0)

		# need to set the layout
		self.setLayout(layout)
		self.adjustSize()

		# tag this widget as a popup
		self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)

		# calculate the botoom right point from the parents rectangle
		point = widget.rect().bottomRight()

		# map that point as a global position
		global_point = widget.mapToGlobal(point)

		# by default, a widget will be placed from its top-left corner, so
		# we need to move it to the left based on the widgets width
		self.move(global_point - QtCore.QPoint(self.width(), 0))

class Window(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.button = QtWidgets.QPushButton('Show', self)
		self.button.clicked.connect(self.handleOpenDialog)
		self.button.move(75, 50)
		self.resize(220, 150)

	def handleOpenDialog(self):
		self.popup = popup(self, self.button)
		self.popup.show()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())