from sage.all import *
from SpaceDecomp import *
from Velocities import *
class Situation:

	#The user will be asked if they want to utilize a situation which has previously been made or if they want to make a new one.	
	def situationLoadOrNew(self):
		response =raw_input('\nPress l to load a situation. \nPress n to create a new situation. \n')
		while response !='l' and response !='n':
			print('This is not a valid input. Please type l/n: ')
			response =raw_input('\nPress l to load a situation. \nPress n to create a new situation. \n')
		if response == 'l':
			return self.chooseSituation()
		if response =='n':
			print('\nYou will now create a new situation.')
			return self.createSituation()
			
	
	
	def chooseSituation(self):
		#We let them load a situation from the Situations folder, and see which situations are in the Situations folder
		#situation = whatever the user chooses
		#return situation
		return 'There is currently no way to save situations. '
	
	
	def createSituation(self):
		#Get a space decomposition
		sd=SpaceDecomp()
		spaceDecomp=sd.spaceDecompLoadOrNew()
		
		#Get a velocity set for this space decomposition
		vel = Velocities(spaceDecomp)
		velocities = vel.createVelocities()
		
		situation = [spaceDecomp,velocities]
		return situation
	
		
	def viewSituation(self):
		#Here a user will be able to view a saved situation in the Situation folder.
		return 'There is currently no way to view saved situations. '
		
		
	def editSituation(self):
		#Here a user will be able to edit a saved situation in the Situation folder.
		return 'There is currently no way to edit saved situations. '

