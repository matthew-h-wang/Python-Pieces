from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

from CodePiece import CodePiece, CodePieceGenerator, CodePieceGeneratorLimited, DragSilhouette
from CodeSpace import CodeLine, CodeSpace, BlockSpace, CodeLinePlus
from FileSaveLoad import MenuBar
from BlockMaker import BlockMaker
from RunCode import CodeRunner



#startblocks = ["print ", "\"Hello World!\"", " var ", " = " ,"--->"]
class Appspace(FloatLayout):
	dragcontroller = ObjectProperty(None)
	workspace = ObjectProperty(None)
	menubar = ObjectProperty(None)

	def __init__(self, **kw):
		super(Appspace, self).__init__(**kw)
#	def __init__(self, **kw):
#		super(Appspace, self).__init__(**kw)


class Workspace(BoxLayout):
	fontsize = NumericProperty(24)
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
		self.blockbox = BoxLayout(orientation = 'vertical')
		self.blockmaker = BlockMaker(workspace = self)

#		self.blockbox.add_widget(self.blockmaker)
		self.blockbox.add_widget(scrollerleft)
		splitter.add_widget(self.blockbox)
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

	def updateFontSize(self, size):
		self.fontsize = size
		# update all generators in blockspace
		for gen in self.blockspace.children:
			gen.font_size = size
		# update all codelines and pieces in codespace
		for codelineplus in self.codespace.children:
			codelineplus.fontsize = size
			codeline = codelineplus.codeline 
			for piece in codeline.children:
				piece.font_size = size

	def updateVersion(self):
		self.parent.menubar.updateVersion()

	def getCode(self):
		text = ''
		for child in self.codespace.children:
			text = child.getLineText() + '\n' + text
		return text

	def getCodeLines(self):
		text = []
		for child in self.codespace.children:
			text.insert(0,child.getLineText())
		return text
		
	def toggleBlockMaker(self):
		if (self.blockmaker in self.blockbox.children):
			self.blockbox.remove_widget(self.blockmaker)
		else:
			self.blockbox.add_widget(self.blockmaker, index=1)

class DragController(Widget):
	pass


class FontSizeSlider(Slider):
	pass

class PythonPiecesApp(App):
	def build(self):
		Window.set_icon('icons/Large-Python-icon.png')
		self.icon = 'icons/Large-Python-icon'

#	def __init__(self, **kw):
#		super(PythonPiecesApp, self).__init__(**kw)
#		self.icon = 'icons/Large-Python-icon' 

if __name__ == '__main__':
	PythonPiecesApp().run()

