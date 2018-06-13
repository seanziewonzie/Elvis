from sage.all import *
from Calculations import *
class Elvis:
	def __init__(self,spaceDecomp):
	self.spaceDecomp = spaceDecomp
	
	def velocitiesLoadOrNew(self):
		#if there are some velocity sets associated with this spaceDecomp, run this
			#self.response =raw_input('Press l to load a velocity set associated with this space decompostion. Press n to create a new one. ')
			#while self.response !='l' and self.response !='n':
				#print('This is not a valid input. Please type l/n: ')
				#self.response =raw_input('Press l to load a velocity set associated with this space decomposition. Press n to create a new one. ')
			#if self.response == 'l':
				#return self.chooseVecloties()
			#if self.response =='n':
				#print('You will now create a new calculation.')
				#return self.createVelocities()
		#if there are no velocity sets associated with this spaceDecomp, run this
			#print (There are no velocity sets associated with this space decomposition. You will now create one. ')
			#return self.createVelocities
		
		return 'We have no coded the creation of velocity sets yet. '
		
		
	def chooseVelocities():
		#Here the user will have the option of seeing the velocity sets saved under this spaceDecomp folder, and choosing one file
		#velocity = whichever file they choose
		#return velocity
		
		return 'We have not coded the saving and loading of velocity sets yet.' 
		
	def createVelocities(self):
		#Here the user will create a velocity set
		#A velocity set is an array of geometric shapes
		#Each geometric shape is associated to a region of the space decomposition. This shape is the set of allowed velocities for the region
		#The velocity set will be created via a for loop, running through each region in spaceDecomp
		
		#Option to save this velocity set under the folder for this spaceDecomp
		
		return 'We have not coded the creation of velocity sets yet. '
