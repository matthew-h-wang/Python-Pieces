from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.button import Button 
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from CodePiece import CodePieceGenerator, CodePiece
from CodeSpace import CodeLinePlus
#import Tkinter
#import tkFileDialog
 
Builder.load_file("FileSaveLoad.kv")

class MenuBar(BoxLayout):
	undoStack = ObjectProperty(None)
	redoStack = ObjectProperty(None)
	maxStackSize = 50	
	currentVersion = None
	savedVersion = None

	def __init__(self, **kw):
		super(MenuBar, self).__init__(**kw)
		self.undoStack = []
		self.redoStack = []

	def loadVersion(self):
		self.undoStack = []
		self.redoStack = []
		self.currentVersion = self.savedVersion
		self.currentVersion.setAsCurrent(self.parent.workspace)

	def saveCurrentVersion(self):
		self.savedVersion = self.currentVersion
		print self.parent.workspace.getCode()


	def updateVersion(self):
		if self.currentVersion:
			self.undoStack.append(self.currentVersion)
		while len(self.undoStack) > self.maxStackSize :
			self.undoStack.pop(0)
		self.currentVersion = Version(self.parent.workspace)
		self.redoStack = []

	def undoLast(self):
		if  len(self.undoStack) == 0:
			return
		self.redoStack.append(self.currentVersion)
		while len(self.redoStack) > self.maxStackSize :
			self.redoStack.pop(0)
		self.currentVersion = self.undoStack.pop()
		self.currentVersion.setAsCurrent(self.parent.workspace)

	def redoLast(self):
		if  len(self.redoStack) == 0:
			return
		self.undoStack.append(self.currentVersion)
		while len(self.undoStack) > self.maxStackSize :
			self.undoStack.pop(0)
		self.currentVersion = self.redoStack.pop()
		self.currentVersion.setAsCurrent(self.parent.workspace)


class FileOpen(Button):
 	def getOpenFileName(self,*args):
 		pass
#	    Tkinter.Tk().withdraw() 
#   	in_path = tkFileDialog.askopenfilename()
#    	print in_path
#    	return in_path



class UndoButton(Button):
	pass
class RedoButton(Button):
	pass


class GeneratorRep:
	text = None
	count = None

	def __init__(self, text, count):
		self.text = text
		self.count = count

	def __repr__(self):
		return  str(self.count) + " " + self.text  

#representation of state of codeSpace and blockSpace, can be used to restore the state of a project
class Version:
	generatorList = [] #list of generator representations
	codeList  = [] #list of code lines, values are lists of IDs that refer to piece list's generators

	def __init__(self, workspace):
		codespace, blockspace = workspace.codespace, workspace.blockspace

		pieceIdDict = {} #keys: instances of generators, values ID numbers
		self.generatorList = []
		self.codeList = []

		i = len(blockspace.children)
		for gen in blockspace.children:
			i -= 1
			pieceIdDict[gen] = i
			rep = GeneratorRep(text = gen.text, count = gen.count)
			self.generatorList.insert(0,rep)

		for codelineplus in codespace.children:
			codeline = codelineplus.codeline
			linelist = []
			for piece in codeline.children:
				id = pieceIdDict[piece.generator]
				linelist.insert(0,id)
			self.codeList.insert(0,linelist)

	#Overwrite workspace with this version
	def setAsCurrent(self, workspace):
		codespace, blockspace = workspace.codespace, workspace.blockspace
		blockspace.clear_widgets()

		idPieceDict = [] #keys: indexes, values: generator instances
		
		#populate the blockspace, keep records on generators
		for rep in self.generatorList:
			generator = CodePieceGenerator(workspace = workspace, start_text = rep.text)
			idPieceDict.append(generator)
			blockspace.add_widget(generator, index = 0)

		codespace.clear_widgets()
		#populate codespace, each line, linking pieces to generators
		for line in self.codeList :
			codelineplus = CodeLinePlus(fontsize = workspace.fontsize)
			codeline = codelineplus.codeline
			for id in line:
				piece = CodePiece(generator = idPieceDict[id])
				codeline.add_widget(piece, index = 0)				
			codespace.add_widget(codelineplus, index = 0)

		codespace.updateLineNums()


	def __repr__(self):
		repr = ""
		i = 0
		for rep in self.generatorList:
			repr += str(i) + " : " + str(rep) + "\n"
			i += 1

		j = 0
		for line in self.codeList:
			j += 1
			repr += str(j) + " :"
			for id in line:
				repr += " " + str(id)  
			repr += "\n"
		return repr

