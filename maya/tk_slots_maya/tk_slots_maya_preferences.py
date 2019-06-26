import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Preferences(Init):
	def __init__(self, *args, **kwargs):
		super(Preferences, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('preferences')

		self.ui.b010.setText(self.hotBox.app.capitalize()+' Preferences')


	def cmb000(self):
		'''
		Select Menu Set
		'''
		cmb = self.ui.cmb000
		
		list_ = ['Modeling', 'Normals', 'Materials', 'UV']
		contents = self.comboBox (cmb, list_)

		index = cmb.currentIndex()
		buttons = self.getObject(self.sb.getUi('main'), 'v000-11')
		for i, button in enumerate(buttons):
			if index==0:
				button.setText(['Extrude','Bridge','Cut','Slice','Delete','Collapse','Insert Loop','Select Loop','Detach','Attach','Chamfer','Target Weld'][i])

			if index==1:
				button.setText(['','','','','','','','','','','',''][i])

			if index==2:
				button.setText(['','','','','','','','','','','',''][i])

			if index==3:
				button.setText(['','','','','','','','','','','',''][i])
				

	def b000(self):
		'''
		Init Tk_Main

		'''
		print "init: tk_main"
		reload(tk_main)

	def b001(self):
		'''
		Color Settings

		'''
		mel.eval('colorPrefWnd;')


	def b002(self):
		'''
		

		'''
		pass


	def b003(self):
		'''
		

		'''
		pass


	def b004(self):
		'''
		

		'''
		pass


	def b005(self):
		'''
		

		'''
		pass


	def b006(self):
		'''
		

		'''
		pass


	def b007(self):
		'''
		

		'''
		pass


	def b008(self):
		'''
		Hotkeys

		'''
		mel.eval("HotkeyPreferencesWindow;")


	def b009(self):
		'''
		Plug-In Manager

		'''
		mel.eval('PluginManager;')


	def b010(self):
		'''
		Settings/Preferences

		'''
		mel.eval("PreferencesWindow;")







#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------