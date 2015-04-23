from os import system

class CodeRunner:
	#proc = None
	
	def startCode(self, filepath, args):
		#if self.proc:
		#	self.stopProc()
		#This is very Windows specific. 
		#self.proc = subprocess.Popen('cmd /K python ' + filepath,  creationflags=subprocess.CREATE_NEW_CONSOLE)
		system("start cmd /C \"python " + filepath + " " + args + " & timeout 86400 /NOBREAK >nul\"")

	#def stopProc(self):
	#	if self.proc:
	#		if self.proc.poll() == None:
	#			print "TRYING TO KILL PROCESS"
	#			self.proc.kill()
	#			self.proc.wait()
	#		self.proc = None
