from sage.all import *
from Calculation import *
from SaveMessage import *
class Velocities:
	def __init__(self,spaceDecomp):
		self.spaceDecomp = spaceDecomp
	
	def velocitiesLoadOrNew(self):
		#if there are some velocity sets associated with this spaceDecomp, run this
		self.response =raw_input('\nPress l to load a velocity set associated with this space decompostion. \nPress n to create a new velocity set associated with this space decompostion. ')
		while self.response !='l' and self.response !='n':
			print('This is not a valid input. Please type l/n: ')
			self.response =raw_input('\nPress l to load a velocity set associated with this space decomposition. \nPress n to create a new velocity set associated with this space decompostion. ')
		if self.response == 'l':
			return self.chooseVecloties()
		if self.response =='n':
			print('You will now create a new velocity set for this space decomposition.')
			return self.createVelocities()

		#if there are no velocity sets associated with this spaceDecomp, run this
			#print (There are no velocity sets associated with this space decomposition. You will now create one. ')
			#return self.createVelocities
		
		
		
	def chooseVelocities(self):
		#Here the user will have the option of seeing the velocity sets saved under this spaceDecomp folder, and choosing one file
		#velocity = whichever file they choose
		#return velocity
		
		return 'We have not coded the saving and loading of velocity sets yet.' 
		
	def createVelocities(self):
		n = self.spaceDecomp[1]

		velocities = []
		for i in range(n):
			while True:
				#For now, velocity sets are just sphere, defined by a real number. This method will have to be rewritten to accept 
				#any function in hyperspherical coordinates.
				try:
					input = (float)(raw_input('\nEnter a positive real number to indicate the velocity associated with region ' +str(i+1) +'. \n'))
					if input > 0:
						break
					else:
						print('This is not a positive number. ')
				except:
					print('Something went wrong. Try again. ')
			velocities.append(input)

		self.saveVelocitySet()
		return velocities

	def saveVelocitySet(self):
		sm = SaveMessage('velocity set')
		sm.message()

		#Option to save this velocity set under the folder for this spaceDecomp
		
