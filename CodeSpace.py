from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from DraggableCodePiece import DraggableCodePiece, DraggableCodePieceGenerator, DraggableCodePiecePlaceholder
from kivy.lang import Builder

Builder.load_file("CodeSpace.kv")

class CodeSpace(StackLayout):
	workspace = ObjectProperty(None)

	def redrawChildren(self, *args) :
		for child in self.children :
			child.redrawChildren()

class CodeLine(StackLayout):

	def redrawChildren(self, *args) :
		for child in self.children :
			child.clear_widgets()
			child.makeDraggableCodePiece()

	workspace = ObjectProperty(None)

class BlockSpace(StackLayout):

	def redrawChildren(self, *args) :
		for child in self.children :
			child.clear_widgets()
			child.makeDraggableCodePiece()

