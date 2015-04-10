from kivy.lang import Builder

from kivy.uix.widget import Widget
from kivy.uix.button import Button 

#import Tkinter
#import tkFileDialog
 
Builder.load_file("FileSaveLoad.kv")

class FileOpen(Button):
 	def getOpenFileName(self,*args):
 		pass
#	    Tkinter.Tk().withdraw() 
#   	in_path = tkFileDialog.askopenfilename()
#    	print in_path
#    	return in_path