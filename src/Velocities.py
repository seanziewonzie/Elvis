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
	

	#The user has decided to choose a velocity set associated with this space decomposition 
	#(and to help them, they can see which velocity sets are in this space decomspoition's folder).
	def chooseVelocities(self):
		#Show the user the chosen velocity sets.		
		os.chdir(os.path.expanduser('~/Documents/ElvisFiles/Situations/'+self.sd.name+'/Velocities/'))
		print "\nYour saved velocity sets:"
		subprocess.call("ls")

		#Let the user choose a velocity file. Keep asking until it works. This code works whether
		#the user types the file extension or not.
		while(True):
			chosenVelFile = Message.getResponse("\nSelect a velocity file (case sensitive): ")
			try:
				with open(chosenVelFile,"r") as file:
					content = file.readlines()
			except:
				try:
					with open(chosenVelFile+'.txt',"r") as file:
						content = file.readlines()
				except:
					if OSError.errno == errno.ENOENT:
						print "---That velocity file does not exist, retry---"
					else:
						Message.errorMessage()
				break
			break
		
		#Populate the variables with information from the text file.
		content = [x.strip() for x in content]
		self.name = content[0]
		self.velocities = ast.literal_eval(content[1])


	#This method will create and return a new velocity set for this space decomposition.
	def createVelocities(self):
		#There will be exactly one velocity set associated to each region in the space decomposition.
		for i in range(self.sd.n):
			#For now, velocity sets are just spheres, defined by a real number. This method will have to be rewritten to accept 
			#any function in hyperspherical coordinates.
			
			#The user will be asked to input a velocity until it is a valid velocity sit which is strictly positive. 
			while True:
				rawNumber = Message.getResponse('\nEnter a positive real number to indicate the velocity associated with region ' +str(i+1) +'. \n')
				try:
					speed = (float)(rawNumber)
				except:
					Message.errorMessage()
					continue
				
				#Check that the number is positive before breaking the loop.	
				if speed > 0:
					break
				else:
					print('This number is not positive. ')
			
			#This is a valid velocity. It is now the velocity associated with region i.
			self.velocities.append(speed)


		#Don't bother asking to save this velocity set if we are not even working with a saved space decomposition.
		if self.sd.name != "":
			self.saveVelocitySet()


	#Save a velocity set as a text file in the folder associated to the relevant space decomposition.
	def saveVelocitySet(self):
		save = Message.getResponse("Save this velocity set(y/n): ")
		while save != "y" and save != "n":
			save = Message.getResponse("Error, type either y or n, retry: ")
		
		#The user decided to save.
		if save == "y":
			#Mark the current directory, so we can return back to it after all of this writing.
			currDir = os.getcwd()

			os.chdir(os.path.expanduser('~/Documents/ElvisFiles/Situations/' + self.sd.name +'/Velocities/'))
			saveDir = os.getcwd()

			#They will keep giving a name to the velocity file until it both makes sense and is not already the name
			#of another saved velocity file.
			while True:
				self.name = Message.getResponse("Name your velocity set. Do not use 'q': ")
				try:
					velFile = open(self.name+'.txt',"w+")
				except:
					if OSError.errno != errno.EEXIST:
						Message.errorMessage()
					else:	
						print "ERROR... Already a saved velocity set. \n"
					continue
				break
			
			#Write all of the relevant information to a text file.
			velFile.write(self.name + "\n")
			velFile.write(str(self.velocities))
			velFile.close()
			
			#Go back to the directory the user was in before this writing process.
			os.chdir(os.path.expanduser(currDir))
			
			#A confirmation message for the user.
			print  self.name + " saved to " + saveDir
