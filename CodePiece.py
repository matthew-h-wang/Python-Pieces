from kivy.lang import Builder
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.core.text import LabelBase

import settings

for font in settings.KIVY_FONTS:
	LabelBase.register(**font)


Builder.load_file("CodePiece.kv")

class CodePieceGenerator(Label):
	workspace = ObjectProperty(None)
	codetext = StringProperty('')
	count = NumericProperty(0)
	bkgdColor = ListProperty([0, 0, 1, 1])
	def __init__(self, workspace, start_text, color, bkgdColor, **kw):
		super(CodePieceGenerator, self).__init__(**kw)
		self.workspace = workspace
		self.codespace = workspace.codespace
		self.font_size = workspace.fontsize
		self.font_name = workspace.fontname
		self.codetext = start_text
		self.color = color
		self.bkgdColor = bkgdColor
		self.count = -1

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):

			ds = self.getDragSilhouette()

			#hacky part: tacken from scatter.py , on_touch_down line 505-508
			self.workspace.parent.dragcontroller.add_widget(ds)
			touch.grab(ds)
			ds._touches.append(touch)
			ds._last_touch_pos[touch] = self.to_window(touch.x, touch.y)

			return True
		return False

	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			generator = self,
			piece = None,
			pos = self.to_window(self.x, self.y))

	def reclaimPiece(self):
		pass

	def decountPiece(self):
		pass

	def whenRemoved(self):
		#remove all code pieces associated with generator
		for codelineplus in self.codespace.children :
			codeline = codelineplus.codeline
			for piece in codeline.children :
				if piece.generator == self:
					codeline.remove_widget(piece)

class CodePieceGeneratorLimited(CodePieceGenerator):
	def __init__(self, workspace, start_text, max_count, color, bkgdColor, **kw):
		super(CodePieceGenerator, self).__init__(**kw)
		self.workspace = workspace
		self.codespace = workspace.codespace
		self.font_size = workspace.fontsize
		self.font_name = workspace.fontname
		self.codetext = start_text
		self.color = color
		self.bkgdColor = bkgdColor
		self.count = max_count


	def reclaimPiece(self):
		self.count += 1

	def decountPiece(self):
		self.count -= 1

	def whenRemoved(self):
		#remove all code pieces associated with generator
		for codelineplus in self.codespace.children :
			codeline = codelineplus.codeline
			for piece in codeline.children :
				if piece.generator == self:
					self.reclaimPiece()
					codeline.remove_widget(piece)

class CodePiece(CodePieceGenerator):
	def __init__(self, generator,**kw):
		super(CodePieceGenerator, self).__init__(**kw)
		self.generator = generator
		self.workspace = generator.workspace
		self.codespace = generator.codespace
		self.font_size = generator.font_size
		self.font_name = generator.font_name
		self.text = generator.codetext
		self.color = generator.color
		self.bkgdColor = generator.bkgdColor
#		self.generator.decountPiece()


	def getDragSilhouette(self):
		return DragSilhouette(source = self, 
			generator = self.generator,
			piece = self,
			pos = self.to_window(self.x, self.y))

	def whenRemoved(self):
		self.generator.reclaimPiece()



class DragSilhouette(Scatter):
	labeltext = StringProperty('')
	my_label = ObjectProperty(None)
	font_size = NumericProperty(20)
	font_name = StringProperty('')
	color = ListProperty([1,1,1,1])
	bkgdColor = ListProperty([0,0,1,1])

	def __init__(self, source, generator, piece, **kw):
		super(DragSilhouette, self).__init__(**kw)
		self.workspace = source.workspace
		self.source = source
		self.labeltext = generator.codetext
		self.codespace = source.codespace
		self.generator = generator
		self.piece = piece
		self.font_size = source.font_size
		self.font_name = source.font_name
		self.color = source.color
		self.bkgdColor = source.bkgdColor

	def on_touch_up(self,touch):
		if not self.parent:
			return

		tx, ty = touch.x, touch.y
		if not touch.grab_current == self:
			return super(DragSilhouette, self).on_touch_up(touch)

		# First: has it moved away from the source (piece or generator)?
		if self.source.collide_point(*self.source.to_widget(tx, ty)) :
			self.parent.remove_widget(self)
			return super(DragSilhouette, self).on_touch_up(touch)

		#if from codepiece, NOT generator
		if self.piece:
			# Next, check if being dropped in the codespace
			newloc = None
			for codelineplus in self.codespace.children :
				if codelineplus.codeline.collide_point(*codelineplus.to_widget(tx, ty)) :
					newloc = codelineplus.codeline
					break

			#If dropped in codespace, move source piece 
			if newloc:	
				ntx, nty = newloc.to_widget(tx, ty)
				# piece indices goes from bottom to top, right to left

				#moving within same line
				if (newloc == self.piece.parent):
					index = 0
					for piece in newloc.children :
						if nty > piece.top or (nty > piece.y and ntx < piece.x):
							index += 1 
						else:
							break
					self.piece.parent.remove_widget(self.piece)
					newloc.add_widget(self.piece, index = index)
				#moving to other line
				else:
					index = 0
					for piece in newloc.children :
						if nty > piece.top or (nty > piece.y and ntx < piece.right):
							index += 1 
						else:
							break
					self.piece.parent.remove_widget(self.piece)
					newloc.add_widget(self.piece, index = index)

				#update version, since either added or moved piece
				self.workspace.updateVersion()

			# if dropped not in codespace, remove piece (if any) from codespace
			else :
				self.piece.parent.remove_widget(self.source)
				self.piece.whenRemoved()
				self.workspace.updateVersion()

		# if from generator
		else:

			# Next, check if being dropped in the codespace
			newloc = None
			for codelineplus in self.codespace.children :
				if codelineplus.codeline.collide_point(*codelineplus.to_widget(tx, ty)) :
					newloc = codelineplus.codeline
					break

			#If dropped in codespace, create new piece 
			if newloc and self.generator.count != 0:

				ntx, nty = newloc.to_widget(tx, ty)
				# piece indices goes from bottom to top, right to left
				index = 0
				for piece in newloc.children :
					if nty > piece.top or (nty > piece.y and ntx < piece.right):
						index += 1 
					else:
						break

				#If from generator, make new piece
				newloc.add_widget(CodePiece(generator=self.generator),
						index = index)
				self.generator.decountPiece()
				#update version, since new piece added
				self.workspace.updateVersion()
			else:
				blockspace = self.generator.workspace.blockspace
				blockmaker = self.generator.workspace.blockmaker
				ntx, nty = blockspace.to_widget(tx, ty)
				ntx2, nty2 = blockmaker.to_widget(tx, ty)
				
				#if dropped in the blockspace, relocate
				if blockspace.collide_point(ntx, nty):
					index = 0
					for gen in blockspace.children :
						#if gen == self.generator:
						#	index += 1
						if nty > gen.top or (nty > gen.y and ntx < gen.x):
							index += 1 
						else:
							break
					blockspace.remove_widget(self.generator)
					blockspace.add_widget(self.generator, index = index)
					self.workspace.updateVersion()
				#if dropped in blockmaker, remove generator and all associated pieces
				elif blockmaker.parent and blockmaker.collide_point(ntx2, nty2):
					blockspace.remove_widget(self.generator)
					self.generator.whenRemoved()
					blockmaker.reclaimBlock(self.generator)
					self.workspace.updateVersion()


			# if dropped not in codespace, blockspace, or blockmaker, do nothing

		self.parent.remove_widget(self)
		return super(DragSilhouette, self).on_touch_up(touch)