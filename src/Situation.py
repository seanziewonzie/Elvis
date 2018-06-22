import sys; sys.dont_write_bytecode = True
from sage.all import *
from SpaceDecomp import *
from Velocities import *
import Message
class Situation:
	def __init__(self):
		self.situation = []
		self.spaceDecompText=[]


	#The user will be asked if they want to utilize a situation which has previously been made or if they want to make a new one.	
	def situationLoadOrNew(self):
		while True:
			response = Message.getResponse('\nPress 1 to load a situation. \nPress 2 to create a new situation. \n')		
			if response != '1' and response != '2':
				print 'Please enter 1 or 2.'
				continue
			break
		if response == '1':
			self.chooseSituation()
		if response =='2':
			print('\nYou will now create a new situation.')
			self.createSituation()
	

	#Here the user will load a situation from the Situations folder.
	def chooseSituation(self):
		while True:
			#Get a saved space decomposition.
			sd=SpaceDecomp()
			sd.chooseSpaceDecomposition()
			spaceDecomp = sd.spaceDecompBackend
			
			#Get a velocity set for this space decomposition.
			vel = Velocities(spaceDecomp)

			#Check that this space decomposition even has velocity sets. If it does not, the user can make one, or choose a different space decomposition.
			#If it does, proceed as normal: choose a velocity set.
			name = spaceDecomp[3]
			list_dir = os.listdir(os.path.expanduser('~/Documents/Elvis/Situation/'+name+'/'))
			count = 0
			for file in list_dir:
				if file.endswith('.vs'): # eg: '.txt'
					count += 1

			if count == 0:
				print 'There are no velocity sets associated to this space decomposition. \n'
				while True:
					response = Message.getResponse('Enter 1 to create a new velocity set for this space decomposition. \nEnter 2 to choose a different space decomposition.\n')
					if response != '1' and response !='2':
						print 'Please enter 1 or 2.'
						continue
					break
				if response =='1':
					velocities = vel.createVelocities()
				if response =='2':
					continue				
			else:
				velocities = vel.chooseVelocities()
			break
		
		self.situation = [spaceDecomp,velocities]
		self.spaceDecompText=sd.spaceDecompText
	
	
	#This creates a situation, which is a space decomposition together with an associated velocity set.
	def createSituation(self):
		#Get a space decomposition
		sd=SpaceDecomp()
		spaceDecomp=sd.spaceDecompLoadOrNew()
		
		#Get a velocity set for this space decomposition
		vel = Velocities(spaceDecomp)
		velocities = vel.createVelocities()
		
		self.situation = [spaceDecomp,velocities]
	
	
	#Here a user chooses to view or edit their chosen situation, or go back to the beginning of the program.
	def viewOrEditSituation(self,situation):
		while True:
			response = Message.getResponse('\nEnter 1 to view text about this situation. \nEnter 2 to edit the velocity set of this situation. \nEnter anything else to go back to the beginning. \n')
			if response == 1:
				viewSituation(situation)
				continue
			if response == 2:
				editSituation(situation)
				continue
			break


	#Here a user will be able to view a saved situation in the Situation folder.
	def viewSituation(self):
		print('There is currently no way to view saved situations. ')
		return []
		

	#Here a user will be able to edit a saved situation in the Situation folder.	
	def editSituation(self):
		print('There is currently no way to edit saved situations. ')
		return []
