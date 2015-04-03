
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
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
			from_generator = True,
			pos = self.pos)

class CodePiece(CodePieceGenerator):

	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			from_generator = False,
			pos = self.pos)

class DragSilhouette(Scatter):
	labeltext = StringProperty('')
	my_label = ObjectProperty(None)
	font_size = NumericProperty(20)

	def __init__(self, source, from_generator, **kw):
		super(DragSilhouette, self).__init__(**kw)
		self.source = source
		self.labeltext = source.text
		self.codespace = source.codespace
		self.from_generator = from_generator
		self.font_size = source.font_size

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

			# piece indices goes from right to left
			index = 0
			for piece in newloc.children :
				if tx < piece.right:
					index += 1 
				else:
					break

			if self.from_generator:
				newloc.add_widget(CodePiece(workspace=self.source.workspace,
					codespace=self.codespace,
					start_text=self.labeltext),
					index = index)
			else :
				# moving within current line to the left
				if (newloc == self.source.parent) and (tx < self.source.x) :
					self.source.parent.remove_widget(self.source)
					newloc.add_widget(self.source, index = (index - 1))
				# moving within current line to the right, or to other line
				else:
					self.source.parent.remove_widget(self.source)
					newloc.add_widget(self.source, index = index)


		self.source.remove_widget(self)
		return super(DragSilhouette, self).on_touch_up(touch)