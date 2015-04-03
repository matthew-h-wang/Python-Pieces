from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

from DraggableCodePiece import DraggableCodePiece, DraggableCodePieceGenerator, DraggableCodePiecePlaceholder
from kivy.lang import Builder

Builder.load_file("CodeSpace.kv")

class CodeSpace(StackLayout):
	workspace = ObjectProperty(None)

	def getWholeText(self):
		text = ''
		linenum = len(self.children)
		for child in self.children:
			text = str(linenum) + ": " + child.getLineText() + '\n' + text
			linenum -= 1
		return text

class CodeLine(StackLayout):
	workspace = ObjectProperty(None)

	def getLineText(self):
		line = ''
		for child in self.children:
			line = child.text + line
		return line

class BlockSpace(StackLayout):
	workspace = ObjectProperty(None)


