from __future__ import print_function
from builtins import super
import os.path

from tk_slots_max_init import *



class Symmetry(Init):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		#symmetry: set initial checked state
		# state = pm.symmetricModelling(query=True, symmetry=True) #application symmetry state
		# axis = pm.symmetricModelling(query=True, axis=True)
		# if axis == "x":
		# 	self.symmetry_ui.chk000.setChecked(state)
		# if axis == "y":
		# 	self.symmetry_ui.chk001.setChecked(state)
		# if axis == "z":
		# 	self.symmetry_ui.chk002.setChecked(state)


	def draggable_header(self, state=None):
		'''Context menu
		'''
		draggable_header = self.symmetry_ui.draggable_header

		if state is 'setMenu':
			draggable_header.contextMenu.add(wgts.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb000(self, index=None):
		'''Editors
		'''
		cmb = self.symmetry_ui.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	@Slots.message
	def setSymmetry(self, state, axis):
		''''''
		# space = "world" #workd space
		# if self.symmetry_ui.chk004.isChecked(): #object space
		# 	space = "object"
		# elif self.symmetry_ui.chk005.isChecked(): #topological symmetry
		# 	space = "topo"

		if axis=='x':
			_axis=0 #0(x), 1,(y), 2(z)
		if axis=='y':
			_axis=1
		if axis=='z':
			_axis=2

		for obj in rt.selection:
			#check if modifier exists
			mod = obj.modifiers[rt.Symmetry]
			if mod==None: #if not create
				mod = rt.symmetry()
				rt.addModifier (obj, mod)
		
			#set attributes
			mod.enabled = state
			mod.threshold = 0.01
			mod.axis = _axis
			mod.flip = negative

		rt.redrawViews()
		return 'Symmetry: '+axis.capitalize()+' <hl>'+str(state)+'</hl>'


	@Slots.sync
	def chk000(self, state=None):
		'''Symmetry X
		'''
		print('chk000')
		self.toggleWidgets(self.childUi, setUnChecked='chk001,chk002')
		state = self.current_ui.chk000.isChecked() #symmetry button state
		self.setSymmetry(state, 'x')


	@Slots.sync
	def chk001(self, state=None):
		'''Symmetry Y
		'''
		self.toggleWidgets(self.childUi, setUnChecked='chk000,chk002')
		state = self.current_ui.chk001.isChecked() #symmetry button state
		self.setSymmetry(state, 'y')


	@Slots.sync
	def chk002(self, state=None):
		'''Symmetry Z
		'''
		self.toggleWidgets(self.childUi, setUnChecked='chk000,chk001')
		state = self.current_ui.chk002.isChecked() #symmetry button state
		self.setSymmetry(state, 'z')


	def chk004(self, state=None):
		'''Symmetry: Object
		'''
		self.symmetry_ui.chk005.setChecked(False) #uncheck symmetry:topological
	

	@Slots.message
	def chk005(self, state=None):
		'''Symmetry: Topo
		'''
		self.symmetry_ui.chk004.setChecked(False) #uncheck symmetry:object space
		# if any ([self.symmetry_ui.chk000.isChecked(), self.symmetry_ui.chk001.isChecked(), self.symmetry_ui.chk002.isChecked()]): #(symmetry)
		# 	pm.symmetricModelling(edit=True, symmetry=False)
		# 	self.toggleWidgets(setUnChecked='chk000-2')
		# 	return 'Note: First select a seam edge and then check the symmetry button to enable topographic symmetry'









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------