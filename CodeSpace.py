from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.button import Button
from CodePiece import CodePiece, CodePieceGenerator, CodePieceGeneratorLimited
from kivy.lang import Builder

Builder.load_file("CodeSpace.kv")

class CodeSpace(StackLayout):
	workspace = ObjectProperty(None)

	def __init__(self, workspace, **kw):
		super(CodeSpace, self).__init__(**kw)
		self.workspace = workspace


	def getWholeText(self):
		text = ''
		linenum = len(self.children)
		for child in self.children:
			text = str(linenum) + ": " + child.getLineText() + '\n' + text
			linenum -= 1
		return text

	def getCode(self):
		text = ''
		for child in self.children:
			text = child.getLineText() + '\n' + text
		return text


	def updateLineNums(self):
		linenum = len(self.children)
		for child in self.children:
			child.linenum = linenum
			linenum -= 1

	#remove given line, unless it's the last one
	def remove_line(self, line):
		if len(self.children) == 1:
			return
		self.remove_widget(line)
		for piece in line.codeline.children:
			piece.whenRemoved()
		self.updateLineNums()

		self.workspace.updateVersion()

	#add a new empty line after given line
	def add_line_after(self, line):
		index = 0
		for codelineplus in self.children:
			if codelineplus != line:
				index += 1
			else:
				break
		self.add_widget(CodeLinePlus(fontsize=self.workspace.fontsize), index)
		self.updateLineNums()

		self.workspace.updateVersion()


	#move the given line to a different position based on touch position
	def move_line(self, line, touch):
		tx, ty = touch.pos		
		index = 0
		for codelineplus in self.children:
			if codelineplus.collide_point(tx, ty):
				self.remove_widget(line)
				self.add_widget(line, index=index)
				self.updateLineNums()
				break
			else:
				index += 1

		self.workspace.updateVersion()




class CodeLinePlus(BoxLayout):
	codeline = ObjectProperty(None)
	draghandle = ObjectProperty(None)
#	newline = ObjectProperty(None)
	removeline = ObjectProperty(None)
	fontsize = NumericProperty(30)
	linenum = NumericProperty(0)

	def getLineText(self):
		return self.codeline.getLineText()	

	def remove_line(self, *args):
		tx, ty = self.removeline.last_touch.pos
		if (self.removeline.collide_point(tx, ty)):
			self.parent.remove_line(self)

#	def add_line(self, *args):
#		tx, ty = self.newline.last_touch.pos
#		if (self.newline.collide_point(tx, ty)):
#			self.parent.add_line_after(self)

	def tap_add(self, *args):
		if (self.draghandle.last_touch.is_triple_tap):
			self.parent.add_line_after(self)
	
	def drag_move(self, *args):
		tx, ty = self.draghandle.last_touch.pos
#		if not self.parent.collide_point(tx, ty):
#			return
		if (self.collide_point(tx, ty)):
			return
		self.parent.move_line(self, self.draghandle.last_touch)


class CodeLine(StackLayout):
	workspace = ObjectProperty(None)
	fontsize = NumericProperty(30)

	def getLineText(self):
		line = ''
		for child in self.children:
			line = child.text + line
		return line

class BlockSpace(StackLayout):
	workspace = ObjectProperty(None)
	def __init__(self, workspace, **kw):
		super(BlockSpace, self).__init__(**kw)
		self.workspace = workspace


