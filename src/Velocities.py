import sys; sys.dont_write_bytecode = True
from sage.all import *
from Calculation import *
import Message
class Velocities:
	def __init__(self,spaceDecomp):
		self.spaceDecomp = spaceDecomp
		self.spaceDecompName = spaceDecomp[3]
		self.velocities = []
		self.name =""
	

	#The user has decided to choose a velocity set associated with this space decomposition. This method will guide the user while they do so,
	#and return the chosen velocity set.			
	def chooseVelocities(self):
		os.chdir(os.path.expanduser('~/Documents/Elvis/Situations/'+self.spaceDecompName+'/'))
		print "\nYour saved velocity sets:\n"
		if platform.system() == "Linux":
			subprocess.call("ls")
		elif platform.system() == "Windows":
			subprocess.call("dir /s")

		while(True):
			try:
				chosenVelFile = raw_input("Select a velocity set (case sensitive): ")
				os.chdir(os.path.expanduser(chosenVelFile))
				break
			except OSError as e:
				if chosenVelFile == 'q':
					print 'quitting...'
					raise SystemExit
				if e.errno == errno.ENOENT:
					print "---That file does not exist, retry---"

		with open(chosenVelFile,"r") as file:
			content = file.readlines()
		self.velocities = ast.literal_eval(content)
		self.name = chosenVelFile


		

	#This method will create and return a new velocity set for this space decomposition.
	def createVelocities(self):
		#There will be exactly one velocity set associated to each region in the space decomposition.
		n = self.spaceDecomp[1]
		for i in range(n):
			while True:
				#The user will be prompted to enter a valid velocity set.
				try:
					#For now, velocity sets are just spheres, defined by a real number. This method will have to be rewritten to accept 
					#any function in hyperspherical coordinates.
					rawNumber = raw_input('\nEnter a positive real number to indicate the velocity associated with region ' +str(i+1) +'. \n')
					speed = (float)(rawNumber)
				except:
					if rawNumber == 'q':
						print 'quitting...'				
						raise SystemExit	
					Message.errorMessage()
					continue
				#Check that the number is positive before breaking the loop.	
				if speed > 0:
					break
				else:
					print('This is not a positive number. ')
			self.velocities.append(speed)

		save = raw_input("Save this Space Decomp(y/n): ")
		if save == 'q':
			print 'quitting...'
			raise SystemExit
		while(True):
			if save != "y" or save != "n":
				save = raw_input("Error, type either y or n, retry: ")
				if save == 'q':
					raise SystemExit
			if save == "y":
				self.saveVelocitySet(self.velocities)
				break





	def saveVelocitySet(self):
		#Save the velocity set as a 
		currDir = os.getcwd()
		os.chdir(os.path.expanduser('~/Documents/Elvis/Situations/' + self.spaceDecompName +'/'))
		saveDir = os.getcwd()
		while True:
			self.name = raw_input("Name your Velocity Set. Do not use 'q': ")
			if self.name == 'q':
				print 'quitting...'
				raise SystemExit	
			try:
				sdFile = open(self.name+'.vs',"w+")
			except OSError as e:
				if e.errno != errno.EEXIST:
					Message.errorMessage()
				else:	
					print "ERROR... Already a saved Decomposition, try again: \n"
				continue
			break

		sdFile.write(str(self.velocities))
		sdFile.close()
		os.chdir(os.path.expanduser(currDir))
		print  self.name + " saved to " + saveDir
