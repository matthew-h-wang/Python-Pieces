from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.button import Button 
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from CodePiece import CodePieceGenerator, CodePiece
from CodeSpace import CodeLinePlus
import tkFileDialog
from Tkinter import Tk
import json


Tk().withdraw()
Builder.load_file("FileSaveLoad.kv")

fileoptions = {}
fileoptions['defaultextension'] = 'pyp'
fileoptions['filetypes'] = [('PythonPieces files', '.pyp'),
							('PythonPieces template file', '.pypt'),
							('all files', '.*')]

class VersionEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, (Version,GeneratorRep)):
			d = {'__class__':obj.__class__.__name__}
			d.update(obj.__dict__)
			return d
		return json.JSONEncoder.default(self, obj)

#class VersionDecoder(json.JSONDecoder):
#	def __init__(self):
#		json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

def dict_to_object(d):
	print "got here"
	if '__class__' in d:
		class_name = d.pop('__class__')
		if class_name == 'Version':
			return Version(genL = d['generatorList'], codeL = d['codeList'])
		elif class_name == 'GeneratorRep':
			return GeneratorRep(text = d['text'], count=d['count'])
		else:
			return None
	else:
		return d

class MenuBar(BoxLayout):
	undoStack = ObjectProperty(None)
	redoStack = ObjectProperty(None)
	maxStackSize = 50	
	currentVersion = None
	savedVersion = None
	currentFileName = None
#	jsonSave = ''

	def __init__(self, **kw):
		super(MenuBar, self).__init__(**kw)
		self.undoStack = []
		self.redoStack = []
		self.currentVersion = Version(lines = 15)

	def loadVersion(self):
		loadfilename = tkFileDialog.askopenfilename(**fileoptions)
		if not loadfilename:
			return
		f = open(loadfilename, 'r')
		loadV =	json.load(f,object_hook=dict_to_object) #TODO make jsonToVersionHook
		if not isinstance(loadV, Version):
			print "Error loading from " + loadfilename
			return
		self.undoStack = []
		self.redoStack = []
		self.currentVersion = loadV
		self.currentVersion.setAsCurrent(self.parent.workspace)
		f.close()
		print "loaded from " + loadfilename

	def saveCurrentVersion(self):
		savefilename = tkFileDialog.asksaveasfilename(**fileoptions)
		if not savefilename:
			return
		self.currentFileName = savefilename
		f = open(savefilename, 'w')
		json.dump(self.currentVersion,f, **{"cls":VersionEncoder}) #TODO make VersionEncoder
		f.close()
		print "saved to " + savefilename

#	def keepCurrentVersionJson(self):
#		self.jsonSave = json.dumps(self.currentVersion, **{"cls":VersionEncoder}) #TODO make VersionEncoder

#	def retrieveCurrentVersionJson(self):
#		v = json.loads(self.jsonSave, object_hook=dict_to_object)
#		print v.toStringDebug()
#		self.currentVersion = v
#		self.currentVersion.setAsCurrent(self.parent.workspace)

	def updateVersion(self):
		if self.currentVersion:
			self.undoStack.append(self.currentVersion)
		while len(self.undoStack) > self.maxStackSize :
			self.undoStack.pop(0)
		self.currentVersion = Version().fromState(self.parent.workspace)
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


class GeneratorRep:
	text = None
	count = None

	def __init__(self, text, count):
		self.text = text
		self.count = count

	def __repr__(self):
		return  str(self.count) + " " + self.text  



#representation of state of codeSpace and blockSpace, can be used to restore the state of a projec

class Version:
	generatorList = [] #list of generator representations
	codeList  = [] #list of code lines, values are lists of IDs that refer to piece list's generators


	def __init__(self, lines = 10, genL = [], codeL = None):
		self.generatorList = genL
		if not codeL:
			self.codeList = []
			for x in range(lines):
				self.codeList.append([])
		else :
			self.codeList = codeL

	#Write Version from the state of the workspace
	def fromState(self, workspace):
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
		return self

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


	def toStringDebug(self):
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
