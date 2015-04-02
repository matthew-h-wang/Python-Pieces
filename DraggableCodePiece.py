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
		print "Made codepiece called " + self.labeltext


	def on_transform_with_touch(self,touch):
		self.current_touch = touch
		return super(DraggableCodePiece, self).on_transform_with_touch(touch)

	def on_touch_up(self,touch):
		if touch == self.current_touch :
			self.current_touch = None
			
			tx, ty = touch.pos
			newloc = None
			for child in self.codespace.children :
				print "looking at codelines"
				if child.collide_point(tx, ty) :
					print "it collides"
					newloc = child
					break

			self.generator.registerDropped(elsewhere=newloc)
			if newloc :
				newloc.add_widget(DraggableCodePiecePlaceholder(workspace=self.generator.workspace,codespace=self.codespace, start_text=self.labeltext))
				newloc.redrawChildren()
						
		return super(DraggableCodePiece, self).on_touch_up(touch)

	
class DraggableCodePieceGenerator(Label):
	workspace = ObjectProperty(None)

	def __init__(self, workspace, codespace, start_text,**kw):
		super(DraggableCodePieceGenerator, self).__init__(**kw)
		self.workspace = workspace
		self.codespace = codespace
		self.text = start_text

	def registerDropped(self, elsewhere=None):
		self.makeDraggableCodePiece()

	def makeDraggableCodePiece(self, *args):
		self.clear_widgets()
		self.add_widget(DraggableCodePiece(generator = self, start_text = self.text, 
			codespace = self.codespace, pos = self.pos))

class DraggableCodePiecePlaceholder(DraggableCodePieceGenerator):

	def registerDropped(self, elsewhere=None):
		if not elsewhere:
			self.makeDraggableCodePiece()
		else:
			self.clear_widgets()
			self.parent.remove_widget(self)

