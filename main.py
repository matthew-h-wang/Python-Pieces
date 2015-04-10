from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.uix.scrollview import ScrollView
from CodePiece import CodePiece, CodePieceGenerator, DragSilhouette
from CodeSpace import CodeLine, CodeSpace, BlockSpace, CodeLinePlus
from FileSaveLoad import FileOpen


startblocks = ["print ", "\"Hello World!\"", " var ", " = " ,"--->","print ", "\"Hello World!\"", " var ", " = " ,"--->","print ", "\"Hello World!\"", " var ", " = " ,"--->","print ", "\"Hello World!\"", " var ", " = " ,"--->","print ", "\"Hello World!\"", " var ", " = " ,"--->"]

class Appspace(FloatLayout):
	dragcontroller = ObjectProperty(None)

	pass

class Workspace(BoxLayout):
	fontsize = NumericProperty(28)
	fontname = StringProperty('Consolas')
	codespace = ObjectProperty(None)
	blockspace = ObjectProperty(None)

	def __init__(self, **kw):
		super(Workspace, self).__init__(**kw)


		self.blockspace = BlockSpace(fontsize = self.fontsize)
		#self.blockspace.bind(minimum_height=self.blockspace.setter('height'))
		splitter = Splitter(sizable_from = 'bottom')
		scrollerleft = ScrollView()
		scrollerleft.add_widget(self.blockspace)
		splitter.add_widget(scrollerleft)
		self.add_widget(splitter)

		self.codespace = CodeSpace(fontsize = self.fontsize)
		scrollerright = ScrollView()
		scrollerright.add_widget(self.codespace)
		self.add_widget(scrollerright)
#		self.add_widget(self.codespace)

		for x in startblocks:
			generator = CodePieceGenerator(workspace = self, start_text = x)
			self.blockspace.add_widget(generator)

		for x in range(1, 15) :
			self.codespace.add_widget(CodeLinePlus(fontsize = self.fontsize))
		self.codespace.updateLineNums()

		
class DragController(Widget):
	pass

class PythonPiecesApp(App):
	pass  

if __name__ == '__main__':
	PythonPiecesApp().run()

