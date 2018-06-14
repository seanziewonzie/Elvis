from sage.all import *
from Situation import *
from StartAndEnd import *
from SaveMessage import *
class Calculation:
	
	#The user will be asked if they want to utilize a calculation which has previously been made or if they want to make a new one.	
	def calculationLoadOrNew(self):
		response =raw_input('\nPress l to load a calculation. \nPress n to create a new calculation. \n')
		while response !='l' and response !='n':
			print('This is not a valid input. Please type l/n: ')
			response =raw_input('\nPress l to load a calculation. \n Press n to create a new calculation. \n')
		if response == 'l':
			return self.chooseSpaceDecomp()
		if response =='n':
			print('\nYou will now create a new calculation.')
			return self.createCalculation()
	
	
	def handleCalculation(self,calculation):
		return 'We have not coded any options to handle calculations'
		#Here they will have the option of deleting calculations, getting a text description of a calculation, 
		#plotting 2-D and maybe 3-D calculations, merging calculations, renaming calculations, and maybe more
	

	def chooseCalculation(self):
		#We let them load a calculation from the Calculations folder, and see which Calculations are in the Calculation folder
		#calculation = whatever the user chooses
		#return calculation
		return 'We have not coded save and write yet'
		



	def createCalculation(self):
		#get the situation
		sit = Situation()
		situation = sit.situationLoadOrNew()



		#get start and end points within this space decomposition
		sae = StartAndEnd(situation)
		startAndEnd = sae.createStartAndEnd()
		
		#With these three specifications, the optimal path problem is well defined
		input = [situation,startAndEnd]
		
		calculation = self.Optimization(input)
		
		self.saveCalculation()
			
		return calculation


	def Optimization(self,input):
		#This classifies and enumerates all paths in our space decomposition from the start point to the end point
		#In fact, it only classifies the ones worthy of consideration
		paths = input[0][0][2].all_paths(input[1][0][1],input[1][1][1])
		p = len(paths)
		if p == 0:
			print ('There are no paths between the starting point and the ending point.\n')
		for i in range(p):
			print('Calculus goes here. ')
		
		#for each path in the array paths, the next bit will define a function based off the velocity sets and number of paths
		#Then it will optimize the function (constrained to only choose boundary points between the regions in the path) 
		#Specifically, it will find the sequence of boundary points which causes the best time, and the time in particular
		
		#From this for loop, we will generate an array of duples - each duple indicates the choice of boundary points and the time they cause
		
		#Find the best time from all the elements in the array
		
		#optimalAnswer will be the duple with the best time
		
		#return optimalAnswer
		
		return 'We have not yet coded a way to find an optimal path'

	def saveCalculation(self):
		sm = SaveMessage('calculation')
		sm.message()
