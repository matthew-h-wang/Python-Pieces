from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.button import Button

from DraggableCodePiece import DraggableCodePiece, DraggableCodePieceGenerator, DraggableCodePiecePlaceholder
from kivy.lang import Builder

Builder.load_file("CodeSpace.kv")

class CodeSpace(StackLayout):
	workspace = ObjectProperty(None)
	fontsize = NumericProperty(30)

	def getWholeText(self):
		text = ''
		linenum = len(self.children)
		for child in self.children:
			text = str(linenum) + ": " + child.getLineText() + '\n' + text
			linenum -= 1
		return text

class CodeLinePlus(BoxLayout):
	codeline = ObjectProperty(None)
	draghandle = ObjectProperty(None)
	newline = ObjectProperty(None)
	removeline = ObjectProperty(None)
	fontsize = NumericProperty(30)

	def getLineText(self):
		return self.codeline.getLineText()	

	def remove_line(self, *args):
		tx, ty = self.removeline.last_touch.pos
		if (self.removeline.collide_point(tx, ty)):
			self.parent.remove_widget(self)

	def add_line(self, *args):
		tx, ty = self.newline.last_touch.pos
		if (self.newline.collide_point(tx, ty)):
			index = 0
			for codelineplus in self.parent.children:
				if codelineplus != self:
					index += 1
				else:
					break
			self.parent.add_widget(CodeLinePlus(fontsize=self.fontsize), index)
	
	def move_line(self, *args):
		tx, ty = self.draghandle.last_touch.pos
		if (self.collide_point(tx, ty)):
			return
		index = 0
		for codelineplus in self.parent.children:
			if codelineplus.collide_point(tx, ty):
				break
			else:
				index += 1
		parent = self.parent
		parent.remove_widget(self)
		parent.add_widget(self, index=index)


class CodeLine(StackLayout):
	workspace = ObjectProperty(None)
	fontsize = NumericProperty(30)

	def getLineText(self):
		line = ''
		for child in self.children:
			line = child.text + line
		return line

class BlockSpace(StackLayout):
	workspace = ObjectProperty(None)
	fontsize = NumericProperty(30)


