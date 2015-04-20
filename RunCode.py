import subprocess
import os

class CodeRunner:
	#proc = None
	
	def startCode(self, filepath, args):
		#if self.proc:
		#	self.stopProc()
		#This is very Windows specific. 
		#self.proc = subprocess.Popen('cmd /K python ' + filepath,  creationflags=subprocess.CREATE_NEW_CONSOLE)
		os.system("start cmd /K python " + filepath + " " + args)

	#def stopProc(self):
	#	if self.proc:
	#		if self.proc.poll() == None:
	#			print "TRYING TO KILL PROCESS"
	#			self.proc.kill()
	#			self.proc.wait()
	#		self.proc = None
