from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from CodePiece import CodePieceGenerator, CodePieceGeneratorLimited
from kivy.lang import Builder

import re

Builder.load_file("BlockMaker.kv")

class BlockMaker(GridLayout):
	workspace = ObjectProperty(None)
	textinput = ObjectProperty(None)
	togglelimit = ObjectProperty(None)
	limittext = ObjectProperty(None)
	colordrop = ObjectProperty(None)
	colorbutton = ObjectProperty(None)

	color = [1,1,1,1]
	bkgdColor = [0,0,1,1]
	def __init__(self, workspace,**kw):
		super(BlockMaker, self).__init__(**kw)
		self.workspace = workspace
		self.colordrop = ColorDropDown()
		self.colordrop.bind(on_select=self.set_colorbutton)

	def set_colorbutton(self,color, *args):
		print "are we getting here"
		self.colorbutton.color = self.color #fix this later

	def makeBlock(self):
		if self.textinput.text == '':
			return

		gen = None
		if self.togglelimit.state == 'normal':
			gen = CodePieceGenerator(workspace=self.workspace, start_text = self.textinput.text,
				color = self.color, bkgdColor = self.bkgdColor)
		elif self.limittext.text != '':
			gen = CodePieceGeneratorLimited(workspace=self.workspace, start_text = self.textinput.text, 
				color = self.color, bkgdColor = self.bkgdColor, max_count= int(self.limittext.text))
		else:
			return
		self.workspace.blockspace.add_widget(gen)
		self.textinput.text = ''
		self.workspace.updateVersion()

class MyInput(TextInput):
	pass
#	def on_text_validate(self, **kw):
#		r = super(MyTextInput, self).on_text_validate(**kw)
#		self.focus = True
#		return r

class IntegerInput(MyInput):
	pat = re.compile('[^0-9]')
	def insert_text(self, substring, from_undo=False):
		pat = self.pat
		s = re.sub(pat, '', substring)
		return super(IntegerInput, self).insert_text(s, from_undo=from_undo)

class ColorButton(Button):
	pass

class ColorDropDown(DropDown):
	pass