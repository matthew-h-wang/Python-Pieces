from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

from CodePiece import CodePieceGenerator, CodePieceGeneratorLimited

import re

colormap = {'Red':[1,0,0,1], 'Blue':[0,0,1,1], 'Green':[0,1,0,1]}

Builder.load_file("BlockMaker.kv")

class BlockMaker(GridLayout):
	workspace = ObjectProperty(None)
	textinput = ObjectProperty(None)
	limittext = ObjectProperty(None)
	colorbutton = ObjectProperty(None)
	colorset = ObjectProperty(None)
	bkgdcolorset = ObjectProperty(None)
	color = [1,1,1,1]
	bkgdColor = [0,0,1,1]
	def __init__(self, workspace,**kw):
		super(BlockMaker, self).__init__(**kw)
		self.workspace = workspace
		self.colorset = ColorSet(self)
		self.bkgdcolorset = BkgdColorSet(self)

	def is_text_focused(self):
		return self.textinput.focus or self.limittext.focus

	def toggle_colorset(self):
		if not (self.colorset in self.children):
			self.add_widget(self.colorset, index = 1)
		else:
			self.remove_widget(self.colorset)

		if not (self.bkgdcolorset in self.children):
			self.add_widget(self.bkgdcolorset, index=1)
		else:
			self.remove_widget(self.bkgdcolorset)

	def makeBlock(self):
		if self.textinput.text == '':
			return

		gen = None
		if self.limittext.text == '':
			gen = CodePieceGenerator(workspace=self.workspace, start_text = self.textinput.text,
				color = self.colorbutton.color, bkgdColor = self.colorbutton.background_color)
		elif int(self.limittext.text) != 0:
			gen = CodePieceGeneratorLimited(workspace=self.workspace, start_text = self.textinput.text, 
				color = self.colorbutton.color, bkgdColor = self.colorbutton.background_color, max_count= int(self.limittext.text))
		else:
			return
		self.workspace.blockspace.add_widget(gen)
		self.textinput.text = ''
		self.workspace.updateVersion()
	def reclaimBlock(self, block):
		self.textinput.text = block.codetext
		self.colorbutton.color = block.color
		self.colorbutton.background_color = block.bkgdColor
		if block.count == -1:
			self.limittext.text = ''
		else:
			self.limittext.text = str(block.count)

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


class ColorSet(GridLayout):
	maker = ObjectProperty(None)

	def __init__(self, maker,**kw):
		super(ColorSet, self).__init__(**kw)
		self.maker = maker


class ColorSetButton(Button):

	def updateButton(self):
		self.parent.maker.colorbutton.color = self.color

class BkgdColorSet(GridLayout):
	maker = ObjectProperty(None)

	def __init__(self, maker,**kw):
		super(BkgdColorSet, self).__init__(**kw)
		self.maker = maker


class BkgdColorSetButton(Button):

	def updateButton(self):
		self.parent.maker.colorbutton.background_color = self.background_color
#		self.parent.maker.bkgdcolorbutton.background_color = self.background_color