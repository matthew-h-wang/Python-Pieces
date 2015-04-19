import subprocess

class CodeRunner:
	proc = None
	
	def startCode(self, filepath):
		if self.proc:
			self.stopProc()
		self.proc = subprocess.Popen('python ' + filepath, )

	def stopProc(self):
		if self.proc:
			if self.proc.poll() == None:
				print "TRYING TO KILL PROCESS"
				self.proc.kill()
				self.proc.wait()
			self.proc = None
