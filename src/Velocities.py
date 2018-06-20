import sys; sys.dont_write_bytecode = True
from sage.all import *
from Calculation import *
from SaveMessage import *
from ErrorMessage import *
class Velocities:
	def __init__(self,spaceDecomp):
		self.spaceDecomp = spaceDecomp
	

	def velocitiesLoadOrNew(self):
		#if there are some velocity sets associated with this spaceDecomp, run this
			#self.response =raw_input('\nPress 1 to load a velocity set associated with this space decompostion. \nPress 2 to create a new velocity set associated with this space decompostion. ')
			#while response != 1 and response !=2
				#self.response =raw_input('Please enter 1 or 2. \nPress 1 to load a velocity set associated with this space decompostion. \nPress 2 to create a new velocity set associated with this space decompostion. ')
			#if self.response == '1':
				#return self.chooseVelocities()
			#if self.response =='2':
				#print('You will now create a new velocity set for this space decomposition.')
				#return self.createVelocities()

		#if there are no velocity sets associated with this spaceDecomp, run this
		print('There are no velocity sets associated with this space decomposition. You will now create one. ')
		return self.createVelocities()
		
			
	def chooseVelocities(self):
		#Here the user will have the option of seeing the velocity sets saved under this spaceDecomp folder, and choosing one file
		#velocity = whichever file they choose
		#return velocity
		print('We have not coded the saving and loading of velocity sets yet.' )
		return []
		

	#This method will create a new velocity set for this space decomposition.
	def createVelocities(self):
		#There will be exactly one velocity set associated to each region in the space decomposition.
		n = self.spaceDecomp[1]
		velocities = []
		for i in range(n):
			while True:
				#The user will be prompted to enter a valid velocity set.
				try:
					#For now, velocity sets are just sphere, defined by a real number. This method will have to be rewritten to accept 
					#any function in hyperspherical coordinates.
					rawNumber = raw_input('\nEnter a positive real number to indicate the velocity associated with region ' +str(i+1) +'. \n')
					speed = (float)(rawNumber)
				except:
					if rawNumber == 'q':
						raise SystemExit	
					err=ErrorMessage()
					err.errorMessage()
					continue
				#Check that the number is positive before breaking the loop.	
				if speed > 0:
					break
				else:
					print('This is not a positive number. ')
			velocities.append(speed)

		#self.saveVelocitySet()
		return velocities


	def saveVelocitySet(self):
		sm = SaveMessage('velocity set')
		sm.message()