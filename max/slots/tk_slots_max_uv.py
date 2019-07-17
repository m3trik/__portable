import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Uv(Init):
	def __init__(self, *args, **kwargs):
		super(Uv, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('uv')




	def cmb000(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb000

		contents = self.comboBox (cmb, ["UV Editor", "UV Set Editor", "UV Tool Kit", "UV Linking: Texture-Centric", "UV Linking: UV-Centric", "UV Linking: Paint Effects/UV", "UV Linking: Hair/UV"], '::')

		index = cmb.currentIndex()
		if index !=0: #hide hotbox then perform operation
			self.hotBox.hide_()
			if index == 1: #UV Editor
				maxEval('TextureViewWindow;') 
			if index == 2: #UV Set Editor
				maxEval('uvSetEditor;')
			if index == 3: #UV Tool Kit
				maxEval('toggleUVToolkit;')
			if index == 4: #UV Linking: Texture-Centric
				maxEval('textureCentricUvLinkingEditor;')
			if index == 5: #UV Linking: UV-Centric
				maxEval('uvCentricUvLinkingEditor;')
			if index == 6: #UV Linking: Paint Effects/UV
				maxEval('pfxUVLinkingEditor;')
			if index == 7: #UV Linking: Hair/UV
				mel.evel('hairUVLinkingEditor;')
			self.ui.cmb000.setCurrentIndex(0)


	def b000(self):
		'''
		Cut Uv Hard Edges
		'''
		mel.eval("tk_cutUvHardEdge ();")


	def b001(self):
		'''
		Flip Uv
		'''
		mel.eval("performPolyForceUV flip 0;")


	def b002(self):
		'''
		
		'''
		pass


	def b003(self):
		'''
		Uv Shell Selection Mask
		'''
		pm.selectType (meshUVShell=1)


	def b004(self):
		'''
		Uv Selection Mask
		'''
		pm.selectType (polymeshUV=1)


	def b005(self):
		'''
		Cut Uv'S
		'''
		pm.polyMapCut()


	def b006(self):
		'''
		
		'''
		pass


	def b007(self):
		'''
		Display Checkered Pattern
		'''
		self.toggleMaterialOverride(checker=1)		


	def b008(self):
		'''
		Adjust Checkered Size
		'''
		mel.eval("bt_textureEditorCheckerSize;")


	def b009(self):
		'''
		Borders
		'''
		maxEval('''
		textureWindowCreatePopupContextMenu "polyTexturePlacementPanel1popupMenusShift";
		int $borders[] = `polyOptions -query -displayMapBorder`;
		float $borderWidth[] = `optionVar -query displayPolyBorderEdgeSize`;
		polyOptions -displayMapBorder (!$borders[0]) -sizeBorder $borderWidth[1];
		''')


	def b010(self):
		'''
		Distortion
		'''
		maxEval('''
		string $winName[] = `getPanel -scriptType polyTexturePlacementPanel`;
		int $state = `textureWindow -query -displayDistortion $winName[0]`;
		if ($state != 1)
			textureWindow -edit -displayDistortion 1 $winName[0];
		else
			textureWindow -edit -displayDistortion 0 $winName[0];
		''')


	def b011(self):
		'''
		Sew Uv'S
		'''
		pm.polyMapSew()


	def b012(self):
		'''
		Auto Unwrap
		'''
		scaleMode = self.ui.chk000.isChecked() #0 No scale is applied. 1 Uniform scale to fit in unit square. 2 Non proportional scale to fit in unit square.
		createNewMap = self.ui.chk001.isChecked() #Create a new UV set, as opposed to editing the current one, or the one given by the -uvSetName flag.
		objects = pm.ls(selection=1, objectsOnly=1, flatten=1) #get shape nodes

		for obj in objects:
			try:
				pm.polyAutoProjection (obj, layoutMethod=0, optimize=1, insertBeforeDeformers=1, scaleMode=scaleMode, createNewMap=createNewMap,
					projectBothDirections=0, #If "on" : projections are mirrored on directly opposite faces. If "off" : projections are not mirrored on opposite faces. 
					layout=2, #0 UV pieces are set to no layout. 1 UV pieces are aligned along the U axis. 2 UV pieces are moved in a square shape.
					planes=6, #intermediate projections used. Valid numbers are 4, 5, 6, 8, and 12
					percentageSpace=0.2, #percentage of the texture area which is added around each UV piece.
					worldSpace=0) #1=world reference. 0=object reference.
			except:
				pass
 

	def b013(self):
		'''
		Auto Map Multiple
		'''
		maxEval('bt_autoMapMultipleMeshes;')


	def b014(self):
		'''
		Rotate On Last
		'''
		maxEval('bt_checkSelectionOrderPref; bt_rotateUVsAroundLastWin;')


	def b015(self):
		'''
		Flip Horizontally On Last
		'''
		maxEval('bt_checkSelectionOrderPref; bt_polyflipUVsAcrossLast 0;')


	def b016(self):
		'''
		Flip Vertically On Last
		'''
		maxEval('bt_checkSelectionOrderPref; bt_polyflipUVsAcrossLast 1;')


	def b017(self):
		'''
		Align Uv Shells
		'''
		self.try_('from AlignUVShells import *; AlignUVShellsWindow()')
		

	def b018(self):
		'''
		Unfold Uv'S
		'''
		maxEval('performUnfold 0;')


	def b019(self):
		'''
		Optimize Uv'S
		'''
		maxEval('performPolyOptimizeUV 0;')


	def b020(self):
		'''
		Move To Uv Space
		'''
		u = str(self.ui.s000.value())
		v = str(self.ui.s001.value())

		pm.polyEditUV (u=u, v=v)


	def b021(self):
		'''
		Straighten Uv
		'''
		maxEval('texStraightenUVs "UV" 30;')


	def b022(self):
		'''
		Stack Similar
		'''
		pm.polyUVStackSimilarShells (to=0.1)









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

#apply uv map
# maxEval('modPanel.addModToSelection (Uvwmap ()) ui:on')