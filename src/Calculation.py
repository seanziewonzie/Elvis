from sage.all import *
from SpaceDecomp import *
from Velocities import *
from StartAndEnd import *
class Calculation:
	global response
	response =""
	global calculation
	calculation = []
	
	def __init__(self):
		self.response = response
		self.calculation = calculation
	
	#The user will be asked if they want to utilize a calculation which has previously been made or if they want to make a new one.	
	def calculationLoadOrNew(self):
		self.response =raw_input('Press l to load a calculation. Press n to create a new one. ')
		while self.response !='l' and self.response !='n':
			print('This is not a valid input. Please type l/n: ')
			self.response =raw_input('Press l to load a calculation. Press n to create a new one. ')
		if self.response == 'l':
			return self.chooseSpaceDecomp()
		if self.response =='n':
			print('You will now create a new calculation.')
			return self.createCalculation()
	
	
	def handleCalculation(self,calculation):
		return 'We have not coded any options to handle calculations'
		#Here they will have the option of deleting calculations, getting a text description of a calculation, 
		#plotting 2-D and maybe 3-D calculations, merging calculations, renaming calculations, and maybe more
	

	def chooseCalculation():
		return 'We have not coded save and write yet'
		#We let them load a calculation from the Calculations folder, and see which Calculations are in the Calculation folder
		#self.calculation = whatever the user chooses
		#return self.calculation



	def createCalculation():
		#Get a space decomposition
		sd=SpaceDecomp()
		spaceDecomp=sd.spaceDecompLoadOrNew()
		
		#Get a velocity set for this space decomposition
		vel = Velocities()
		velocities = vel.velocitiesLoadOrNew(spaceDecomp)
		
		#get start and end points within this space decomposition
		sae = StartAndEnd
		startAndEnd = sae.createStartAndEnd(spaceDecomp)
		
		#With these three specifications, the optimal path problem is well defined
		situation = [spaceDecomp,velocities,startAndEnd]
		
		self.calculation = optimization(situation)
		
		saveOption = raw_input('Enter s to save this calculation. Enter anything else to move on. ')
		if saveOption == 's':
			print('Saving calculations is not a feature yet. ')
			
		return self.calculation


	def optimization(situation):
		#This classifies and enumerates all paths in our space decomposition from the start point to the end point
		#In fact, it only classifies the ones worthy of consideration
		paths = situation[0][2].all_paths(situation[2][0],situation[2][1])
		
		#for each path in the array paths, the next bit will define a function based off the velocity sets and number of paths
		#Then it will optimize the function (constrained to only choose boundary points between the regions in the path) 
		#Specifically, it will find the sequence of boundary points which causes the best time, and the time in particular
		
		#From this for loop, we will generate an array of duples - each duple indicates the choice of boundary points and the time they cause
		
		#Find the best time from all the elements in the array
		
		#optimalAnswer will be the duple with the best time
		
		#return optimalAnswer
		
		return 'We have not yet coded a way to find an optimal path'
