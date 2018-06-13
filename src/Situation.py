from sage.all import *
from SpaceDecomp import *
from Velocities import *
from StartAndEnd import *
class Situation:

	#The user will be asked if they want to utilize a situation which has previously been made or if they want to make a new one.	
	def situationLoadOrNew(self):
		response =raw_input('Press l to load a situation. Press n to create a new one. ')
		while response !='l' and response !='n':
			print('This is not a valid input. Please type l/n: ')
			response =raw_input('Press l to load a situation. Press n to create a new one. ')
		if response == 'l':
			return self.chooseSituation()
		if response =='n':
			print('You will now create a new calculation.')
			return self.createSituation()
			
	
	
	def chooseSituation():
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
	
		
	def viewSituation(self)
		#Here a user will be able to view a saved situation in the Situation folder.
		return 'There is currently no way to view saved situations. '
		
		
	def editSituation(self)
		#Here a user will be able to edit a saved situation in the Situation folder.
		return 'There is currently no way to edit saved situations. '
	
