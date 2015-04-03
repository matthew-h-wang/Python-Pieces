from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from CodePiece import CodePiece, CodePieceGenerator, DragSilhouette
from CodeSpace import CodeLine, CodeSpace, BlockSpace


class Workspace(FloatLayout):

	def __init__(self, **kw):
		super(Workspace, self).__init__(**kw)
		self.codespace = CodeSpace()
		self.add_widget(self.codespace)
		for x in range(1, 5) :
			self.codespace.add_widget(CodeLine())

#		codeline = CodeLine()
#		codeline.add_widget(DraggableCodePiecePlaceholder(workspace = self, codespace = self.codespace, start_text = "Hello "))
#		codeline.add_widget(DraggableCodePiecePlaceholder(workspace = self, codespace = self.codespace, start_text = "Goodbye"))
#		self.codespace.add_widget(codeline)
#		self.codespace.redrawChildren()
		

		self.blockspace = BlockSpace()
		self.add_widget(self.blockspace)

		generator = CodePieceGenerator(workspace = self, codespace = self.codespace, start_text = "Hello ")
		self.blockspace.add_widget(generator)
		print "first generator added"
		generator2 = CodePieceGenerator(workspace = self, codespace = self.codespace, start_text = "World ")
		self.blockspace.add_widget(generator2)

class PythonPiecesApp(App):
	pass  

if __name__ == '__main__':
	PythonPiecesApp().run()

