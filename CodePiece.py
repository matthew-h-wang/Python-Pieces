
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.text import LabelBase
import settings

for font in settings.KIVY_FONTS:
	LabelBase.register(**font)


Builder.load_file("CodePiece.kv")

class CodePieceGenerator(Label):
	workspace = ObjectProperty(None)


	def __init__(self, workspace, start_text,**kw):
		super(CodePieceGenerator, self).__init__(**kw)
		self.workspace = workspace
		self.codespace = workspace.codespace
		self.font_size = workspace.fontsize
		self.font_name = workspace.fontname
		self.text = start_text

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):

			ds = self.getDragSilhouette()
			#self.add_widget(ds)
			#ds.pos = self.workspace.parent.dragcontroller.to_widget(self.x, self.y)
			#hacky part: tacken from scatter.py , on_touch_down line 505-508
			self.workspace.parent.dragcontroller.add_widget(ds)

			ds._bring_to_front()
			touch.grab(ds)
			ds._touches.append(touch)
			ds._last_touch_pos[touch] = self.to_window(touch.x, touch.y)

			return True
		return False

	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			from_generator = True,
			pos = self.to_window(self.x, self.y))

class CodePiece(CodePieceGenerator):

	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			from_generator = False,
			pos = self.to_window(self.x, self.y))

class DragSilhouette(Scatter):
	labeltext = StringProperty('')
	my_label = ObjectProperty(None)
	font_size = NumericProperty(20)
	font_name = StringProperty('')

	def __init__(self, source, from_generator, **kw):
		super(DragSilhouette, self).__init__(**kw)
		self.source = source
		self.labeltext = source.text
		self.codespace = source.codespace
		self.from_generator = from_generator
		self.font_size = source.font_size
		self.font_name = source.font_name

	def on_touch_up(self,touch):
		tx, ty = touch.x, touch.y
		if not touch.grab_current == self:
			return super(DragSilhouette, self).on_touch_up(touch)

		# First: has it moved away from the generator?
		if self.source.collide_point(*self.source.to_widget(tx, ty)) :
			self.parent.remove_widget(self)
			return super(DragSilhouette, self).on_touch_up(touch)

		# Next, check if being dropped in the codespace
		newloc = None
		for codelineplus in self.codespace.children :
			if codelineplus.codeline.collide_point(*codelineplus.to_widget(tx, ty)) :
				newloc = codelineplus.codeline
				break

		#If dropped in codespace, either create new piece or move source piece 
		if newloc:	
			ntx, nty = newloc.to_widget(tx, ty)
			# piece indices goes from bottom to top, right to left
			index = 0
			for piece in newloc.children :
				if nty > piece.top or (nty > piece.y and ntx < piece.right):
					index += 1 
				else:
					break

			if self.from_generator:
				newloc.add_widget(CodePiece(workspace=self.source.workspace,
					start_text=self.labeltext),
					index = index)
			else :
				# moving within current line to the left
				if (newloc == self.source.parent) and \
						(nty > self.source.top or \
						(nty > self.source.y and ntx < self.source.x )) :
					self.source.parent.remove_widget(self.source)
					newloc.add_widget(self.source, index = (index - 1))
				# moving within current line to the right, or to other line
				else:
					self.source.parent.remove_widget(self.source)
					newloc.add_widget(self.source, index = index)

		# if dropped elsewhere, remove source if from codespace
		else :
			if not self.from_generator:
				self.source.parent.remove_widget(self.source)

		self.parent.remove_widget(self)
		return super(DragSilhouette, self).on_touch_up(touch)