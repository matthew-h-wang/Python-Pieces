from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from CodePiece import CodePieceGenerator
from kivy.lang import Builder


Builder.load_file("BlockMaker.kv")

class BlockMaker(BoxLayout):
	workspace = ObjectProperty(None)
	textinput = ObjectProperty(None)
	
	def __init__(self, workspace,**kw):
		super(BlockMaker, self).__init__(**kw)
		self.workspace = workspace


	def makeBlock(self):
		gen = CodePieceGenerator(workspace=self.workspace, start_text = self.textinput.text)
		self.workspace.blockspace.add_widget(gen)
		self.workspace.updateVersion()

