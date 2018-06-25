import sys; sys.dont_write_bytecode = True
from sage.all import *
import os
import errno
import subprocess
import re
import platform
import Message
import ast
class Velocities:
	def __init__(self,sd):
		self.velocities = []
		self.name =""
		self.sd=sd
	

	#The user has decided to choose a velocity set associated with this space decomposition. This method will guide the user while they do so,
	#and return the chosen velocity set.			
	def chooseVelocities(self):
		os.chdir(os.path.expanduser('~/Documents/Elvis/Situations/'+self.sd.name+'/'))
		print "\nYour saved velocity sets:\n"
		if platform.system() == "Linux":
			subprocess.call("ls")
		elif platform.system() == "Windows":
			subprocess.call("dir /s")

		while(True):
			chosenVelFile = Message.getResponse("Select a velocity file (case sensitive): ")
			try:
				with open(chosenVelFile,"r") as file:
					content = file.readlines()
				break
			except OSError as e:
				pass
			try:
				with open(chosenVelFile+'.text',"r") as file:
					content = file.readlines()
				break
			except OSError as e:
				if e.errno == errno.ENOENT:
					print "---That velocity file does not exist, retry---"
				else:
					Message.errorMessage()
		content = [x.strip() for x in content]
		self.name = content[0]
		self.velocities = ast.literal_eval(content[1])



		

	#This method will create and return a new velocity set for this space decomposition.
	def createVelocities(self):
		#There will be exactly one velocity set associated to each region in the space decomposition.
		for i in range(self.sd.n):
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

		if self.sd.name != "":
			save = Message.getResponse("Save this velocity set(y/n): ")
			while save != "y" and save != "n":
				save = Message.getResponse("Error, type either y or n, retry: ")
			if save == "y":
				self.saveVelocitySet()


	#Save a velocity set file in the folder associated to the relevant space decomposition.
	def saveVelocitySet(self):
		#Save the velocity set as a 
		currDir = os.getcwd()
		os.chdir(os.path.expanduser('~/Documents/Elvis/Situations/' + self.sd.name +'/'))
		saveDir = os.getcwd()
		while True:
			self.name = Message.getResponse("Name your velocity set. Do not use 'q': ")
			try:
				velFile = open(self.name+'.text',"w+")
			except OSError as e:
				if e.errno != errno.EEXIST:
					Message.errorMessage()
				else:	
					print "ERROR... Already a saved velocity set. \n"
				continue
			break
		velFile.write(self.name + "\n")
		velFile.write(str(self.velocities))
		velFile.close()
		os.chdir(os.path.expanduser(currDir))
		print  self.name + " saved to " + saveDir
