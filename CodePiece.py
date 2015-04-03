
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file("CodePiece.kv")

class CodePieceGenerator(Label):
	workspace = ObjectProperty(None)

	def __init__(self, workspace, codespace, start_text,**kw):
		super(CodePieceGenerator, self).__init__(**kw)
		self.workspace = workspace
		self.codespace = codespace
		self.text = start_text

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):

			ds = self.getDragSilhouette()
			self.add_widget(ds)
			#hacky part: tacken from scatter.py , on_touch_down line 505-508
			ds._bring_to_front()
			touch.grab(ds)
			ds._touches.append(touch)
			ds._last_touch_pos[touch] = touch.pos
			return True
		return False

	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			start_text = self.text,
			from_generator = True,
			codespace = self.codespace, 
			pos = self.pos)

class CodePiece(CodePieceGenerator):

	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			start_text = self.text,
			from_generator = False,
			codespace = self.codespace, 
			pos = self.pos)

class DragSilhouette(Scatter):
	labeltext = StringProperty('')
	my_label = ObjectProperty(None)

	def __init__(self, codespace, source, from_generator, start_text,**kw):
		super(DragSilhouette, self).__init__(**kw)
		self.labeltext = start_text
		self.source = source
		self.codespace = codespace
		self.from_generator = from_generator

	def on_touch_up(self,touch):
		tx, ty = touch.x, touch.y
		if not touch.grab_current == self:
			return super(DragSilhouette, self).on_touch_up(touch)

		# First: has it moved away from the generator?
		if self.source.collide_point(tx, ty) :
			self.source.remove_widget(self)
			return super(DragSilhouette, self).on_touch_up(touch)

		# Next, check if being dropped in the codespace
		newloc = None
		for child in self.codespace.children :
			if child.collide_point(tx, ty) :
				newloc = child
				break

		#If dropped in codespace, either create new piece or move source piece 
		if newloc:	
			if self.from_generator:
				newloc.add_widget(CodePiece(workspace=self.source.workspace,codespace=self.codespace, start_text=self.labeltext))
			else :
				self.source.parent.remove_widget(self.source)
				newloc.add_widget(self.source)

		self.source.remove_widget(self)
		return super(DragSilhouette, self).on_touch_up(touch)