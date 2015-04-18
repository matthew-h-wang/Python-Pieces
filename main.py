from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.uix.scrollview import ScrollView
from CodePiece import CodePiece, CodePieceGenerator, CodePieceGeneratorLimited, DragSilhouette
from CodeSpace import CodeLine, CodeSpace, BlockSpace, CodeLinePlus
from FileSaveLoad import MenuBar
from BlockMaker import BlockMaker

#startblocks = ["print ", "\"Hello World!\"", " var ", " = " ,"--->"]
class Appspace(FloatLayout):
	dragcontroller = ObjectProperty(None)
	workspace = ObjectProperty(None)
	menubar = ObjectProperty(None)



class Workspace(BoxLayout):
	fontsize = NumericProperty(28)
	fontname = StringProperty('Consolas')
	codespace = ObjectProperty(None)
	blockspace = ObjectProperty(None)
	blockmaker = ObjectProperty(None)
	def __init__(self, **kw):
		super(Workspace, self).__init__(**kw)

		self.blockspace = BlockSpace(workspace = self)
		splitter = Splitter(sizable_from = 'bottom')
		scrollerleft = ScrollView()
		scrollerleft.add_widget(self.blockspace)
		box = BoxLayout(orientation = 'vertical')
		box.add_widget(scrollerleft)
		self.blockmaker = BlockMaker(workspace = self)
		box.add_widget(self.blockmaker)
		splitter.add_widget(box)
		self.add_widget(splitter)

		self.codespace = CodeSpace(workspace = self)
		scrollerright = ScrollView()
		scrollerright.add_widget(self.codespace)
		self.add_widget(scrollerright)

#		for x in startblocks:
#			generator = CodePieceGenerator(workspace = self, start_text = x)
#			self.blockspace.add_widget(generator)

		for x in range(15) :
			self.codespace.add_widget(CodeLinePlus(fontsize = self.fontsize))
		self.codespace.updateLineNums()

	def updateVersion(self):
		self.parent.menubar.updateVersion()

	def getCode(self):
		text = ''
		for child in self.codespace.children:
			text = child.getLineText() + '\n' + text
		return text
		
class DragController(Widget):
	pass

class PythonPiecesApp(App):
	pass  

if __name__ == '__main__':
	PythonPiecesApp().run()

