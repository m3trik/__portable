from PySide2 import QtCore, QtGui, QtWidgets

import os.path

from tk_switchboard import Switchboard
from tk_styleSheet import StyleSheet






class EventFactoryFilter(QtCore.QObject):
	'''
	Event filter for dynamic ui objects.
	args:
		parent=<parent>
	'''
	__mouseOver = [] #list of widgets currently under the mouse cursor.
	__mouseGrabber = None
	__mouseHover = QtCore.Signal(bool)
	__mousePressPos = QtCore.QPoint()

	enterEvent_ = QtCore.QEvent(QtCore.QEvent.Enter)
	leaveEvent_ = QtCore.QEvent(QtCore.QEvent.Leave)


	def __init__(self, parent=None):
		super(EventFactoryFilter, self).__init__(parent)

		self.sb = Switchboard()
		if parent:
			self.tk = parent



	def init(self, name, widgets=None):
		'''
		Set Initial widget states.
		args:
			name = 'string' - ui name.
			widgets = [list of <QWidgets>] - if no list is given, the operation will be performed on all widgets of the given ui name.
		'''
		if not widgets:
			widgets = self.sb.getWidget(name=name)

		for widget in widgets: #get all widgets for the given ui name.

			widgetName = widget.objectName()
			widgetType = self.sb.getWidgetType(widget, name) #get the class type as string.
			derivedType = self.sb.getDerivedType(widget, name) #get the derived class type as string.

			uiLevel = self.sb.getUiLevel(name)

			if not widget.styleSheet(): #if the widget doesn't already have a styleSheet.
				widget.setStyleSheet(getattr(StyleSheet, derivedType, ''))

			widget.installEventFilter(self)


			if widgetType=='QPushButton' and uiLevel<3:
				self.resizeAndCenterWidget(widget)

			elif widgetType=='QWidget':
				if self.sb.prefix(widgetName, 'r'): #prefix returns True if widgetName startswith the given prefix, and is followed by three integers.
					widget.setVisible(False)

			elif widgetType=='QDoubleSpinBox':
				if name=='create':
					if self.sb.prefix(widgetName, 's'):
						widget.setVisible(False)



	def createPushButton(self, name, objectName, size=None, location=None, text='', whatsThis='', show=True):
		'''
		Create a pushbutton object.
		args:
			name = 'string' - name of the ui where the button is to be placed.
			objectName = 'string' - set button's object name.
			size = [int, int] or <QSize> - button size.
			location = <QPoint> - desired global location.
			text = 'string' - set button text.
			whatsThis = 'string' - set button whatsThis tag.
			show = bool - set button visibility.
		returns:
			the created button.
		'''
		w = QtWidgets.QPushButton(text, self.sb.getUi(name))

		if size:
			try: w.resize(size[0], size[1])
			except:	w.resize(size)
		if location:
			w.move(w.mapFromGlobal(location - w.rect().center())) #move and center
		if show:
			w.show()
		if whatsThis:
			w.setWhatsThis(whatsThis)

		self.sb.addWidget(name, w, objectName)
		self.init(name, [w]) #initialize the widget to set things like the event filter and styleSheet.

		return w



	def resizeAndCenterWidget(self, widget, padding=30):
		'''
		Adjust the given widget's width to fit contents and re-center.
		args:
			widget = <widget object> - widget to resize.
			padding = int - additional width to be applied at both ends.
		'''
		x1 = widget.rect().center().x()
		widget.resize(widget.sizeHint().width()+padding, widget.height())
		x2 = widget.rect().center().x()
		diff = x1-x2
		widget.move(widget.x()+diff, widget.y())



	def mouseTracking(self, name):
		'''
		Get widget/s currently under cursor. Grab mouse, and send events accordingly.
		args:
			name = 'string' - ui name.
		'''
		for widget in self.sb.getWidget(name=name): #get all widgets from the current ui.
			widgetName = widget.objectName()

			if widget.rect().contains(widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
				if not widget in self.__mouseOver: #if widget is already in the mouseOver list, no need to re-process the events.
					QtWidgets.QApplication.sendEvent(widget, self.enterEvent_)
					self.__mouseOver.append(widget)

					if not widgetName=='mainWindow':
						widget.grabMouse() #set widget to receive mouse events.
						self.__mouseGrabber = widget

			else:
				if widget in self.__mouseOver: #if widget is in the mouseOver list, but the mouse is no longer over the widget:
					QtWidgets.QApplication.sendEvent(widget, self.leaveEvent_)
					self.__mouseOver.remove(widget)



	@staticmethod
	def createEventName(event):
		'''
		Get an event method name string from a given event.
		ie. 'enterEvent' from QtCore.QEvent.Type.Enter,
		ie. 'mousePressEvent' from QtCore.QEvent.Type.MouseButtonPress
		args:
			event = <QEvent>
		returns:
			'string' - formatted method name
		'''
		e = str(event.type()).split('.')[-1] #get the event name ie. 'Enter' from QtCore.QEvent.Type.Enter
		e = e[0].lower() + e[1:] #lowercase the first letter.
		e = e.replace('Button', '') #remove 'Button' if it exists.
		return e + 'Event' #add trailing 'Event'



	def eventFilter(self, widget, event):
		'''
		Forward widget events to event handlers.
		For any event type, the eventfilter will try to connect to a corresponding method derived
		from the event type string.  ie. self.enterEvent(event) from 'QtCore.QEvent.Type.Enter'
		This allows for forwarding of all events without each having to be explicity stated.
		args:
			widget = <QWidget>
			event = <QEvent>
		'''

		eventTypes = [ #types of events to be handled:
			'QEvent',
			'QChildEvent',
			'QResizeEvent',
			'QShowEvent',
			'QHideEvent',
			'QEnterEvent',
			'QLeaveEvent',
			'QKeyEvent',
			'QMouseEvent',
			'QMoveEvent',
			'QHoverEvent',
			'QContextMenuEvent',
			'QDragEvent',
			'QDropEvent',
		]

		if not any([event.__class__.__name__==e for e in eventTypes]): #do not process the event if it is not one of the types listed in 'eventTypes'
			# print event.__class__.__name__
			return False
		# print event.__class__.__name__


		self.widget = widget
		self.name = self.sb.getNameFrom(self.widget) #get the ui name corresponding to the given widget.
		self.widgetName = self.widget.objectName()
		self.widgetType = self.sb.getWidgetType(self.widget, self.name)
		self.derivedType = self.sb.getDerivedType(self.widget, self.name)
		self.mainWindow = self.sb.getWidget('mainWindow', self.name)
		self.uiLevel = self.sb.getUiLevel(self.name)

		eventName = EventFactoryFilter.createEventName(event) #get 'mousePressEvent' from <QEvent>
		# print self.name, eventName, self.widgetType, self.widgetName


		if hasattr(self, eventName):
			getattr(self, eventName)(event) #handle the event locally. #ie. self.enterEvent(event)
			return super(EventFactoryFilter, self).eventFilter(widget, event)
		else:
			return False



	# ------------------------------------------------
	# Events
	# ------------------------------------------------
	def showEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.widgetName=='mainWindow':
			self.widget.activateWindow()

		if self.derivedType=='QComboBox':
			method = self.sb.getMethod(self.name, self.widgetName)
			if callable(method):
				method()



	def hideEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.widgetName=='mainWindow':
			if self.__mouseGrabber:
				self.__mouseGrabber.releaseMouse()
				self.__mouseGrabber = None



	def enterEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.__mouseHover.emit(True)

		if self.widgetType=='QWidget':
			if self.sb.prefix(self.widgetName, 'r'):
				self.widget.setVisible(True) #set visibility

		elif self.widgetType=='QPushButton':
			if self.sb.prefix(self.widgetName, 'i'): #set the stacked widget.
				submenu = self.widget.whatsThis()+'_submenu'
				if not self.name==submenu: #do not reopen the submenu if it is already open.
					self.name = self.tk.setSubUi(self.widget, submenu)

			elif self.widgetName=='<':
				self.tk.setPrevUi()



	def leaveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.__mouseHover.emit(False)

		if self.widget==self.__mouseGrabber: #self.widget.mouseGrabber():
			if self.mainWindow.isVisible():
				self.mainWindow.grabMouse()
				self.__mouseGrabber = self.mainWindow

		if self.widgetType=='QWidget':
			if self.sb.prefix(self.widgetName, 'r'):
				self.widget.setVisible(False) #set visibility



	def mousePressEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		self.__mousePressPos = event.globalPos() #mouse positon at press
		self.__mouseMovePos = event.globalPos() #mouse move position from last press



	def mouseMoveEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		globalPos = event.globalPos()
		diff = globalPos -self.__mouseMovePos
		self.__mouseMovePos = globalPos



	def mouseReleaseEvent(self, event):
		'''
		args:
			event = <QEvent>
		'''
		if self.widget.rect().contains(self.widget.mapFromGlobal(QtGui.QCursor.pos())): #if mouse over widget:
			if self.widgetType=='QPushButton':
				if self.sb.prefix(self.widgetName, 'i'): #ie. 'i012'
					self.tk.setUi(self.widget.whatsThis()) #switch the stacked layout to the given ui.
					self.tk.move(QtGui.QCursor.pos() - self.tk.ui.rect().center()) #move window to cursor position and offset from left corner to center

				elif self.sb.prefix(self.widgetName, 'v'):
					self.sb.previousUi(as_list=1).append(self.sb.getMethod(self.name, self.widgetName)) #store the camera view
					self.widget.click()

				elif self.sb.prefix(self.widgetName, 'b'):
					if '_submenu' in self.name:
						self.widget.click()
					else: #add the buttons command to the prevCommand list.
						self.sb.prevCommand(as_list=1).append([self.sb.getMethod(self.name, self.widgetName), self.sb.getDocString(self.name, self.widgetName)]) #store the command method object and it's docString (ie. 'Multi-cut tool')






#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# p1 = self.widget.mapToGlobal(self.widget.rect().center())

# 					submenu = self.widget.whatsThis()+'_submenu'
# 					n = self.widgetName
# 					if not self.name==submenu: #do not reopen submenu on enter event if it is already open.
# 						self.name = self.tk.setUi(submenu) #switch the stacked layout to the given submenu.
# 						self.widget = getattr(self.tk.currentWidget(), n) #get the widget with the same name in the new ui.


# 						p3 = self.tk.mapToGlobal(self.tk.pos())
# 						p2 = self.widget.mapToGlobal(self.widget.rect().center())
# 						self.tk.move(self.tk.mapFromGlobal(p3 +(p1 - p2)))



# print name, self.sb.previousName(as_list=1)[-3]
					# if name==self.sb.previousName(as_list=1, allowDuplicates=1)[-3]: #if index is changed to the previous ui, remove the last widget.
						# del self.prevWidget[-1:]


#show button for any previous commands.
		# if self.sb.prefix(self.widgetName, 'v') and self.name=='main': #'v024-29'
		# 	self.widget.setText(self.sb.prevCommand(docString=1, as_list=1)[-num]) #prevCommand docString
		#  	#self.resizeAndCenterWidget(self.widget)
		# 	self.widget.show()