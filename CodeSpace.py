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

	def 

	def remove_self(self, *args):
		tx, ty = self.removeline.last_touch.pos
		if (self.removeline.collide_point(tx, ty)):
			self.parent.remove_widget(self)



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


