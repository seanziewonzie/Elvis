	def save(self):
		if t == "y":
			#change working dir to /home/Documents
			os.chdir(os.path.expanduser("~/Documents"))
			try:
				#try and change working dir to /home/Documents/ElvisData
				os.chdir(os.path.expanduser("~/Documents/ElvisData"))
			except OSError as error:
				#if /home/Documents/ElvisData doesn't exits, create the dir in /home/Documents/
				if error.errno == errno.ENOENT:
					subprocess.call(["mkdir","ElvisData"]) 
				#change working dir to /home/Documents/ElvisData          
				os.chdir(os.path.expanduser("~/Documents/ElvisData"))
			finally:
				#create a file in /home/Documents/ElvisData
				subprocess.call(["touch",str(self.d)+"-dimens_"+str(self.n)+"-regions"+".txt"])


	if __name__ == "__main__":
		getGraph()
		save()
