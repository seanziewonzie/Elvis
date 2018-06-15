from sage.all import *
from SpaceDecomp import *
from Velocities import *
from ErrorMessage import errorMessage
class Situation:

	#The user will be asked if they want to utilize a situation which has previously been made or if they want to make a new one.	
	def situationLoadOrNew(self):
		response =raw_input('\nPress 1 to load a situation. \nPress 2 to create a new situation. \n')		
		while response !=1 and response !=2:
			response =raw_input('Please enter 1 or 2. \nPress 1 to load a situation. \nPress 2 to create a new situation. \n')
		if response == '1':
			return self.chooseSituation()
		if response =='2':
			print('\nYou will now create a new situation.')
			return self.createSituation()
			
	
	#Here the user will load a situation from the Situations folder.
	def chooseSituation(self):
		#Get a saved space decomposition.
		sd=SpaceDecomp()
		spaceDecomp=sd.chooseSpaceDecomposition()
		
		#Get a velocity set for this space decomposition
		vel = Velocities(spaceDecomp)
		velocities = vel.chooseVelocities()
		
		situation = [spaceDecomp,Velocities]
		return situation
	
	
	#This creates a situation, which is a space decomposition together with an associated velocity set.
	def createSituation(self):
		#Get a space decomposition
		sd=SpaceDecomp()
		spaceDecomp=sd.spaceDecompLoadOrNew()
		
		#Get a velocity set for this space decomposition
		vel = Velocities(spaceDecomp)
		velocities = vel.createVelocities()
		
		situation = [spaceDecomp,velocities]
		return situation
	
	
	#Here a user chooses to view or edit their chosen situation, or go back to the beginning of the program.
	def viewOrEditSituation(self,situation):
		response = raw_input('\nEnter 1 to view text about this situation. \nEnter 2 to edit the velocity set of this situation. \nEnter 3 to go back to the beginning. \n')
		while response != 1 and response !=2 and response !=3:
			print('Please enter 1 or 2 or 3. \nEnter 1 to view text about this situation. \nEnter 2 to edit this situation. \nEnter 3 to go back to the beginning. \n')
		if response == 1:
			viewSituation(situation)
		if response == 2:
			editSituation(situation)
		return response



	#Here a user will be able to view a saved situation in the Situation folder.
	def viewSituation(self):
		return 'There is currently no way to view saved situations. '
		

	#Here a user will be able to edit a saved situation in the Situation folder.	
	def editSituation(self):
		return 'There is currently no way to edit saved situations. '

