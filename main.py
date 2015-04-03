from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from CodePiece import CodePiece, CodePieceGenerator, DragSilhouette
from CodeSpace import CodeLine, CodeSpace, BlockSpace


startblocks = ["print ", "\"Hello World!\"", " var ", " = " ,"--->"]

class Workspace(FloatLayout):
	fontsize = NumericProperty(20)

	def __init__(self, **kw):
		super(Workspace, self).__init__(**kw)
		self.codespace = CodeSpace()
		self.add_widget(self.codespace)
		for x in range(1, 15) :
			self.codespace.add_widget(CodeLine())

		self.blockspace = BlockSpace()
		self.add_widget(self.blockspace)

		for x in startblocks:
			generator = CodePieceGenerator(workspace = self, codespace = self.codespace, start_text = x)
			self.blockspace.add_widget(generator)
		
class PythonPiecesApp(App):
	pass  

if __name__ == '__main__':
	PythonPiecesApp().run()

