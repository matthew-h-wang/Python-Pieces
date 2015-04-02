from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from DraggableCodePiece import DraggableCodePiece, DraggableCodePieceGenerator, DraggableCodePiecePlaceholder
from CodeSpace import CodeLine, CodeSpace


class Workspace(FloatLayout):

	def __init__(self, **kw):
		super(Workspace, self).__init__(**kw)
		self.codespace = CodeSpace()
		self.add_widget(self.codespace)
		self.codespace.add_widget(CodeLine())
		codeline = CodeLine()
		codeline.add_widget(DraggableCodePiecePlaceholder(workspace = self, codespace = self.codespace, start_text = "Hello "))
		codeline.add_widget(DraggableCodePiecePlaceholder(workspace = self, codespace = self.codespace, start_text = "Goodbye"))
		self.codespace.add_widget(codeline)
		self.codespace.redrawChildren()
		generator = DraggableCodePieceGenerator(workspace = self, codespace = self.codespace, start_text = "Hello World")
		self.add_widget(generator)
		generator.makeDraggableCodePiece()



class PythonPiecesApp(App):
	pass  

if __name__ == '__main__':
	PythonPiecesApp().run()

