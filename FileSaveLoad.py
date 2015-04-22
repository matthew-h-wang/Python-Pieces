from kivy.lang import Builder
#from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button 
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown 
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.slider import Slider

from CodePiece import CodePieceGenerator, CodePieceGeneratorLimited, CodePiece
from CodeSpace import CodeLinePlus
from RunCode import CodeRunner

import tkFileDialog
from Tkinter import Tk
import json
import os.path 

Tk().withdraw()
Builder.load_file("FileSaveLoad.kv")

fileoptions = {}
fileoptions['defaultextension'] = '.pyp'
fileoptions['filetypes'] = [('PythonPieces files', '.pyp'),
							('PythonPieces template file', '.pypt'),
							('all files', '.*')]

insertString = "#INSERTHERE#"

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
	if '__class__' in d:
		class_name = d.pop('__class__')
		if class_name == 'Version':
			return Version(genL = d['generatorList'], codeL = d['codeList'])
		elif class_name == 'GeneratorRep':
			return GeneratorRep(text = d['text'], count=d['count'], color = d['color'], bkgdColor =d['bkgdColor'])
		else:
			return None
	else:
		return d

class MenuBar(FloatLayout):
	undoStack = ObjectProperty(None)
	redoStack = ObjectProperty(None)
	maxStackSize = 50	
	currentVersion = None
	currentFileName = None

	loadB = ObjectProperty(None)
	reloadB = ObjectProperty(None)
	saveB = ObjectProperty(None)
	saveAsB = ObjectProperty(None)
	undoB = ObjectProperty(None)
	redoB = ObjectProperty(None)
	runB = ObjectProperty(None)
	settingsB = ObjectProperty(None)
	settingspanel = ObjectProperty(None)
	argsInput = ObjectProperty(None)
#	stopB = ObjectProperty(None)

	def __init__(self, **kw):
		super(MenuBar, self).__init__(**kw)
		self.undoStack = []
		self.redoStack = []
		self.currentVersion = Version(lines = 15)
		self.coderunner = CodeRunner()

		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)
		self.lctrlPress = False
		self.rctrlPress = False
		self.rshiftPress = False
		self.shiftPress = False

		self.settingspanel = DropDown()
		self.fontslider = FontSizeSlider()
		self.fontslider.bind(on_value = self.updateFontSize)
		self.settingspanel.add_widget(self.fontslider)

#		App.get_running_app().bind(on_stop = self.stopCode)

	def updateFontSize(self):
		self.parent.workspace.updateFontSize(self.fontslider.value)

	def saveAndRunCode(self):
		codefilename = self.saveCode()
		
		if not codefilename:
			return None
		self.coderunner.startCode(codefilename, self.argsInput.text)


#	def stopCode(self):
#		self.coderunner.stopProc()

	def saveCode(self):
		if not self.currentFileName:
			return None
		savefilename = self.currentFileName + '.py'
		f = open(savefilename, 'w')
		codeTemplatefilename = self.currentFileName + '.pypc'

		if os.path.isfile(codeTemplatefilename):
			
			with open(codeTemplatefilename, 'r') as fc:
				codelines = self.parent.workspace.getCodeLines()
				for line in fc:
					if insertString in line:
						#get indentation
						tabs = line.split(insertString)[0]
						#insert code here
						for cline in codelines:
							f.write(tabs + cline + "\n")
					else:
						f.write(line)

		else: #just write code to file
			codestring = self.parent.workspace.getCode()
			f.write(codestring)
		
		f.close()
		print "saved code to " + savefilename
		return savefilename

	def loadVersion(self):
		loadfilename = tkFileDialog.askopenfilename(**fileoptions)
		if not loadfilename:
			return None
		f = open(loadfilename, 'r')
		loadV =	json.load(f,object_hook=dict_to_object) 
		if not isinstance(loadV, Version):
			print "Error loading from " + loadfilename
			return None
		self.undoStack = []
		self.redoStack = []
		self.currentFileName, ext = os.path.splitext(loadfilename)
		self.currentVersion = loadV
		self.currentVersion.setAsCurrent(self.parent.workspace)
		f.close()
		self.undoB.pressable = False
		self.redoB.pressable = False
		self.saveB.pressable = True
		templatefilename = self.currentFileName + '.pypt'
		self.reloadB.pressable = os.path.isfile(templatefilename)

		print "loaded from " + loadfilename
		self.get_root_window().set_title(loadfilename)
		return loadfilename

	def reloadFromTemplate(self):
		if not self.currentFileName:
			return None
		loadfilename = self.currentFileName + '.pypt'
		if not os.path.isfile(loadfilename):
			print "No template to load from"
			return None
		f = open(loadfilename, 'r')
		loadV =	json.load(f,object_hook=dict_to_object) 
		if not isinstance(loadV, Version):
			print "Error loading from " + loadfilename
			return None
		self.undoStack.append(self.currentVersion)
		self.currentVersion = loadV
		self.redoStack = []
		self.currentVersion.setAsCurrent(self.parent.workspace)
		f.close()
		self.undoB.pressable = True
		self.redoB.pressable = False
		print "reloaded from " + loadfilename
		self.get_root_window().set_title(loadfilename)
		return loadfilename

	def saveCurrentVersionAs(self):
		savefilename = tkFileDialog.asksaveasfilename(**fileoptions)
		if not savefilename:
			return None
		self.currentFileName, ext = os.path.splitext(savefilename)
		f = open(savefilename, 'w')
		json.dump(self.currentVersion,f, **{"cls":VersionEncoder})
		f.close()
		self.saveB.pressable = False
		print "saved to " + savefilename
		self.get_root_window().set_title(savefilename)
		return savefilename

	def saveCurrentVersion(self):
		if not self.currentFileName:
			self.saveB.pressable = False
			return None
		savefilename = self.currentFileName + '.pyp'
		f = open(savefilename, 'w')
		json.dump(self.currentVersion,f, **{"cls":VersionEncoder}) 
		f.close()
		self.saveB.pressable = False
		print "saved to " + savefilename
		self.get_root_window().set_title(savefilename)
		return savefilename

	def updateVersion(self):
		if self.currentVersion:
			self.undoStack.append(self.currentVersion)
		while len(self.undoStack) > self.maxStackSize :
			self.undoStack.pop(0)
		self.currentVersion = Version().fromState(self.parent.workspace)
		self.redoStack = []
		if self.currentFileName:
			self.saveB.pressable = True
		self.undoB.pressable = True
		self.redoB.pressable = False
		

	def undoLast(self):
		if  len(self.undoStack) == 0:
			return
		self.redoStack.append(self.currentVersion)
		while len(self.redoStack) > self.maxStackSize :
			self.redoStack.pop(0)
		self.currentVersion = self.undoStack.pop()
		self.currentVersion.setAsCurrent(self.parent.workspace)
		self.saveB.pressable = True
		self.redoB.pressable = True
		self.undoB.pressable = True if (len(self.undoStack) > 0) else False

	def redoLast(self):
		if  len(self.redoStack) == 0:
			return
		self.undoStack.append(self.currentVersion)
		while len(self.undoStack) > self.maxStackSize :
			self.undoStack.pop(0)
		self.currentVersion = self.redoStack.pop()
		self.currentVersion.setAsCurrent(self.parent.workspace)
		self.saveB.pressable = True
		self.undoB.pressable = True
		self.redoB.pressable = True if len(self.redoStack) > 0 else False


	#These keyboard shortcuts are based in Windows standards
	def _keyboard_closed(self):
		pass
#		self._keyboard.unbind(on_key_down = self._on_keyboard_down)
#		self._keyboard.unbind(on_key_up = self._on_keyboard_up)
#		self._keyboard = None

	def _on_keyboard_up(self, keyboard, keycode):
		if keycode[1] == 'lctrl':
			self.lctrlPress = False
		elif keycode[1] == 'rctrl':
			self.rctrlPress = False
		elif keycode[1] == 'shift':
			self.shiftPress = False
		elif keycode[1] == 'rshift':
			self.rshiftPress = False
		return True


	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'lctrl':
			self.lctrlPress = True
		elif keycode[1] == 'rctrl':
			self.rctrlPress = True
		elif keycode[1] == 'shift':
			self.shiftPress = True
		elif keycode[1] == 'rshift':
			self.rshiftPress = True
		else :
			if not (self.lctrlPress or self.rctrlPress) :
				return True

			if keycode[1] == 's':
				if (self.shiftPress or self.rshiftPress):
					self.saveCurrentVersionAs()
				else:
					self.saveCurrentVersion()
			elif keycode[1] == 'o':
				self.loadVersion()
			elif keycode[1] == 'z' :
				#if blockmaker has text focus, don't override the undo
				if not self.parent.workspace.blockmaker.is_text_focused() :	
					self.undoLast()
			elif keycode[1] == 'u':
				self.undoLast()
			elif keycode[1] == 'y':
				self.redoLast()
			elif keycode[1] == 'r':
				#if blockmaker has text focus, don't override the redo
				if not self.parent.workspace.blockmaker.is_text_focused() :
					self.redoLast()

			elif keycode[1] == 'backspace':
				if (self.shiftPress or self.rshiftPress):
					self.reloadFromTemplate()
			elif keycode[1] == 'enter':
				if (self.shiftPress or self.rshiftPress):
					self.stopCode()
				else:
					self.saveAndRunCode()
		return True



class GeneratorRep:
	text = None
	count = None
	color = None
	bkgdColor = None

	def __init__(self, text, count, color, bkgdColor):
		self.text = text
		self.count = count
		self.color = color
		self.bkgdColor = bkgdColor
	def __repr__(self):
		return  str(self.count) + " " + self.text + " " + str(self.color) + " " + str(self.bkgdColor)



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
			rep = GeneratorRep(text = gen.codetext, count = gen.count, color=gen.color, bkgdColor = gen.bkgdColor)
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
			generator = None
			if rep.count >= 0:
				generator = CodePieceGeneratorLimited(workspace = workspace, start_text = rep.text, 
								color = rep.color, bkgdColor = rep.bkgdColor, max_count = rep.count) 
			else:
				generator = CodePieceGenerator(workspace = workspace, start_text = rep.text,
								color = rep.color, bkgdColor = rep.bkgdColor)
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


class MenuButton(Button):
	imageSource = StringProperty('')
	hoverText = StringProperty('')
	pressable = BooleanProperty(True)

class MenuSpacer(Widget):
	pass

class FontSizeSlider(Slider):
	pass