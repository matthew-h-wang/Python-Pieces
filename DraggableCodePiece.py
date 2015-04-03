from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file("DraggableCodePiece.kv")

class DraggableCodePiece(Scatter):
	labeltext = StringProperty('')
	my_label = ObjectProperty(None)

	def __init__(self, codespace, generator, start_text,**kw):
		super(DraggableCodePiece, self).__init__(**kw)
		self.labeltext = start_text
		self.generator = generator
		self.current_touch = None
		self.codespace = codespace
		self.reset_position()
		print "Made codepiece called " + self.labeltext

	def reset_position(self):
		print "reset_position called"
		self.pos = self.generator.pos
		print "New position" + str(self.pos)

	def on_transform_with_touch(self,touch):
		self.current_touch = touch
		return super(DraggableCodePiece, self).on_transform_with_touch(touch)

	def on_touch_up(self,touch):
		print "on_touch_up from DraggableCodePiece called"
		if touch == self.current_touch :
			self.current_touch = None
			
			tx, ty = touch.pos
			newloc = None
			# First: has it moved away from the generator?
			if self.generator.collide_point(tx, ty) :
				self.reset_position()
				return super(DraggableCodePiece, self).on_touch_up(touch)

			for child in self.codespace.children :
				print "looking at codelines"
				if child.collide_point(tx, ty) :
					print "it collides"
					newloc = child
					break

			if newloc:
				newloc.add_widget(DraggableCodePiecePlaceholder(workspace=self.generator.workspace,codespace=self.codespace, start_text=self.labeltext))
				print "dude why isn't this working"
				self.generator.registerDropped()

		self.reset_position()
		return super(DraggableCodePiece, self).on_touch_up(touch)

	
class DraggableCodePieceGenerator(Label):
	workspace = ObjectProperty(None)

	def __init__(self, workspace, codespace, start_text,**kw):
		print "constructor called from DraggableCodePieceGenerator"

		super(DraggableCodePieceGenerator, self).__init__(**kw)
		self.workspace = workspace
		self.codespace = codespace
		self.text = start_text
		self.makeDraggableCodePiece()

	def registerDropped(self, elsewhere=None):
		print "registerDropped called from DraggableCodePieceGenerator"
		pass

	def makeDraggableCodePiece(self, *args):
		print "makeDraggableCodePiece called DraggableCodePieceGenerator"
		newpiece =	DraggableCodePiece(generator = self, start_text = self.text, 
			codespace = self.codespace, pos = self.pos)
		#self.bind(pos=newpiece.reset_position())
		self.add_widget(newpiece)

class DraggableCodePiecePlaceholder(DraggableCodePieceGenerator):

	def registerDropped(self, elsewhere=None):
		print "makeDraggableCodePiece called from DraggableCodePiecePlaceholder"

		self.parent.remove_widget(self)
