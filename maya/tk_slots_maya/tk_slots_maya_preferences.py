import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Preferences(Init):
	def __init__(self, *args, **kwargs):
		super(Preferences, self).__init__(*args, **kwargs)




	def b000(self): #init tk_main
			print "init: tk_main"
			reload(tk_main)

	def b001(self): #color settings
		mel.eval('colorPrefWnd;')

	def b002(self): #fbx presets
		mel.eval('FBXUICallBack -1 editExportPresetInNewWindow fbx;')

	def b003(self): #obj presets
		mel.eval('FBXUICallBack -1 editExportPresetInNewWindow obj;')

	def b004(self): #
		mel.eval('')

	def b005(self): #
		mel.eval('')

	def b006(self): #
		mel.eval('')

	def b007(self): #
		mel.eval('')

	def b008(self): #Hotkeys
		mel.eval("HotkeyPreferencesWindow;")

	def b009(self): #Plug-in manager
		mel.eval('PluginManager;')

	def b010(self): #Settings/preferences
		mel.eval("PreferencesWindow;")



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------