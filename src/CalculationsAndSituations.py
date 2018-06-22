import sys; sys.dont_write_bytecode = True
from sage.all import *
from Situation import *
from StartAndEnd import *
from SpaceDecomp import *
from Velocities import *
import Message
import numpy as np

class Calculation:
	def __init__(self):
		self.calculation = []


	#The user will be asked if they want to utilize a calculation which has previously been made or if they want to make a new one.	
	def calculationLoadOrNew(self):
		while True:
			reponse = Message.getResponse('\nPress 1 to load a calculation. \nPress 2 to create a new calculation. \n')
			if response != '1' and response != '2':
				print 'Please enter 1 or 2.'
				continue
			if response == '1':
				self.chooseCalculation()
			if response =='2':
				self.createCalculation()
		return self.calculation


	#With calculation in hand, the user will have the option to do something with it.
	#Currently there are no options.
	#Potential actions: plotting, merging to calculations together to plot them together, deleting, renaming.		
	def handleCalculation(self,calculation):
		while True:
			print 'We have not coded any options to handle calculations'
			response = Message.getResponse('\nEnter 1 to perform another action with this calculation. \nEnter anything else to get go back to the beginning. \n')
			if response == 1:
				continue
			break

	
	#We let them load a calculation from the Calculations folder (and to help them, they can see which calculations are in the Calculation folder).
	#Currently this has not been coded.
	def chooseCalculation(self):
		#Press 1 to load a calculation.
			#Enter name.
			#If it's not a valid name, let them choose 1 or 2 again.
			#If it is, calculation = whatever file the user chooses.
		#Press 2 to see all names of saved calculations.

		#return calculation
		return 'We have not coded save and write yet'
		

	#The user will create a calculation from a situation and a choice of start and end points.
	def createCalculation(self):
		#Get the situation.
		sit = Situation()
		situation = sit.situationLoadOrNew()

		#Get the start and end points within this space decomposition.
		sae = StartAndEnd(situation)
		startAndEnd = sae.createStartAndEnd()
		
		#With these three specifications, the time function is well defined. Send the problem into the Optimization method
		#to get the solution.
		problem = [situation,startAndEnd]
		solution = self.Optimization(problem)

		#A calculation has information about both the problem and its solution.
		self.calculation = [problem,solution]
		
		self.saveCalculation()


	#Given a problem, this method will find the path in the situation from the start point to the endpoint which
	#minimizes the time function.
	def Optimization(self,problem):
		#Unpack all the necessary information.
		d=problem[0][0][0]
		adjGraph=problem[0][0][2]
		velocities = problem[0][1][0]
		startRegion=problem[1][0][1]
		endRegion=problem[1][1][1]
		startCoords=problem[1][0][0]
		endCoords=problem[1][1][0]
		
		#This classifies and enumerates all paths in our space decomposition from the start point to the end point
		#In fact, it only classifies the ones worthy of consideration.
		paths = adjGraph.all_paths(startRegion,endRegion)
		p = len(paths)

		#If p==0, there are no paths at all.
		if p == 0:
			print('\nThere are no paths between the starting point and the ending point.\n')
			return ['No solution.']
		else:
			optimalPaths = []
			optimalTimes = []

			#For each particular class of paths, find the most optimal path among them.
			for k in range(p):
				path = paths[k]
				l = len(path)
				


				#T is the function to minimize. Get it and turn it into a lambda function.
				T=self.functionToMinimize(l,d,velocities)
				S = lambda x: eval(T)

				#Get the constraints this function must be minimized over. We only care about points which are in the 
				#correct interfaces. Turn them into lambda functions.
				constraints=self.getConstraints(l,d,adjGraph,startCoords,endCoords)
				lambdas_list =[]
				for i in range(len(constraints)):
					lambdas_list.append(self.build_lambdas(constraints,i))

				#Get an initial point to do the optimization from.
				initialPoint = self.generateIntialPoint(l,d,adjGraph,startCoords,endCoords)

				#This actually calculates where the function is minimized
				optimalInput = minimize_constrained(S,lambdas_list,initialPoint)

				#Get the optimal time by actually plugging the optimal path into the time function. Now the 2D array of
				#input numbers will take the role of the 2D array of variables, and the functionToMinimize method will 
				#return a value, not a symbolic function
				optimalTime = S(optimalInput)

				#This packs the path into a more readable 2D array rather than one long array.
				optimalPath = []
				for i in range(l+1):
					optimalPath.append(optimalInput[d*i:d*(i+1)])


				
				#Add the optimalPath to the running list of optimal paths.
				optimalPaths.append(optimalPath)

				#Add the optimalTime to the running list of optimal times.
				optimalTimes.append(optimalTime)

			#Get the best time from the best times of all classes of paths, and the path which causes it.	
			bestTime = np.min(optimalTimes)
			bestPathNum = np.argmin(optimalTimes)
			bestPath = optimalPaths[bestPathNum]

			#Print the best path.
			length= len(bestPath)
			print('The best path is as follows:')
			for i in range(length):
				if i== 0:
					print('\nStart at')
				elif i== length:
					print('and end at')
				else:
					print('and head to')
				print bestPath[i]

			print('\nThe best time is: '+ str(bestTime))

			#Package them together and return.
			solution = [bestTime,bestPath]
			return solution

	
	#This function will build a mathematical expression of the time a path from the starting point to the ending point takes 
	#in the situation.
	def functionToMinimize(self,l,d,velocities):
		T = '0'
		for i in range(l):
			#The following loop builds an expression for the distance between one chosen point and the next.
			sqDist='0'
			for j in range(d):
				sqDist = sqDist + '+(x[' +str(d*(i+1)+j)+ ']-x[' +str(d*i+j)+ '])**2'
			
			#The time that one piece of the path contributes (depends on distance and velocity).
			t = '(1.0/' +str(velocities[i])+ ')*sqrt(' + sqDist + ')'
			
			#Add it to the total time function
			T = T+ '+' +t
		return T


	#This will generate an array of "expressions" which correspond to inequalities involving the variables x_i_j. These inequalities
	#will force the function to only be minimized over the class of paths which go between the correct interfaces ("correct" meaning
	#corresponding to the class of paths under consideration).
	def getConstraints(self,l,d,adjGraph,startCoords,endCoords):
		constraints=[]
		#Constrain the first d variables to be the correspond to the coordinates of the starting point. Cast the constraint as
		#a function expression.
		for j in range(d):
			startConstraint1='x['+str(j)+'] -' + str(startCoords[j])

			constraints.append(startConstraint1)

			startConstraint2=str(startCoords[j]) +' - x['+str(j)+']'

			constraints.append(startConstraint2)
		

		#Constrain the last d variables to be the correspond to the coordinates of the ending point. Cast the constraint as
		#a function expression.
		for j in range(d):
			endConstraint1='x['+str(l*d+j)+'] -' + str(endCoords[j])
			constraints.append(endConstraint1)


			endConstraint2=str(endCoords[j]) +'- x['+str(l*d+j)+']'

			constraints.append(endConstraint2)

		#Constain the i-th d-tuple of variables so that they together represent a point which is contained in
		#the intersection of the i-1-th and i-th polyhedron in the path.
		if l >= 2:
			for i in range(1,l): 
				#Get the intersection of polyhedron which this i-th point must lie in.
				exitPoly = adjGraph.get_vertex(i-1)
				enterPoly = adjGraph.get_vertex(i)
				intersection = exitPoly&enterPoly
				#Get the inequalities which define this polyhedron, and apply them to the i-th point.
				constraintsForPoint = self.getConstraintsForSpecificPoint(intersection,i,d)
				#Add this constraint to the running list of constraints.
				constraints = constraints + constraintsForPoint
		
		#Cast the function expressions to "function_type"s. This currently is not working.
		return constraints


	#Get the numerical expressions determined by the polyhedral interface this specific point must lie in to get the constraint.
	def getConstraintsForSpecificPoint(self,intersection,i,d):	
		#Get a representation of the inequalities which bound this polyhedron.			
		a = intersection.Hrepresentation()
		length = len(a)
		array = []
		for m in range(length):
			#The Hrepresentation is a weird object that is an array of some sort of pickled strings describing
			#the hspaces in prose, rather than just as numbers. This will unpack it into an easy-to-use array.
			string = str(a[m])
			b = string.split(" ")
			b = b[2:-2]
			b[0] = b[0][1:-1]
			for j in range(d-1):
				b[j+1] = b[j+1][:-1]
			b.remove('x')
			
			#With this new array, generate an expression which would represent what exactly is >=0 in this inequality.
			constraint = '0'
			negConstraint='0'
			for j in range(d):
				constraint = constraint + '+' + str(float(b[j])) +'*x['+str(d*i+j)+']'
				negConstraint = negConstraint + '-' + str(float(b[j])) +'*x['+str(d*i+j)+']'
			
			#Add the final constant to the function expression.
			if b[d] == '+':
				constraint = constraint + '+ ' +str(float(b[d+1]))
				negConstraint = negConstraint + '- ' +str(float(b[d+1]))
			if b[d] == '-':
				constraint = constraint + '- '+ str(float(b[d+1]))
				negConstraint = negConstraint + '+ '+ str(float(b[d+1]))


			#If it is an equality, break it up into two over-determined inequalities. Add the inequalit(y/ies) to the array
			#of constraints.
			if "equation" in str(a[m]):
				array.append(constraint)
				array.append(negConstraint)
			if "inequality" in str(a[m]):
				array.append(constraint)
		return array
				
	
	#Convert constraints into lambdas.
	def build_lambdas(self,constraints,i):
		return lambda x: eval(constraints[i])


	#This will generate an inital point to begin the optimization process.			
	def generateIntialPoint(self,l,d,adjGraph,startCoords,endCoords):
		initialPoint = []
		
		#The first d coordinates must correspond to the starting point
		for j in range(d):
			initialPoint.append(startCoords[j])
		
		if l>=2:
			#The middle d-tuples must correspond to points which are part of the corresponsing interfaces.
			#This is what representative_point accomplishes.
			for i in range(1,l):
				exitPoly = adjGraph.get_vertex(i-1)
				enterPoly = adjGraph.get_vertex(i)
				intersection =exitPoly&enterPoly
				referencePoint = intersection.representative_point()
				for j in range(d):
					initialPoint.append(referencePoint[j])
		
		#The final d coordinates must correspond to the ending point
		for j in range(d):
			initialPoint.append(endCoords[j])
		
		return initialPoint


	def saveCalculation(self):
		while True:
			self.name = raw_input("Name your calculation: ")
			currDir = os.getcwd()
			os.chdir(os.path.expanduser('~/Documents/Elvis/Calculations'))
			try:
				os.makedirs(self.name)
				os.chdir(os.path.expanduser(self.name))
				saveDir = os.getcwd()
			except OSError as e:
				if e.errno != errno.EEXIST:
					Message.errorMessage()
				else:	
					print "ERROR... Already a saved calculation, try again: \n"
				continue
			break

		sdFile = open("Space_Decomp_Info.txt","w+")
		sdFile.write(str(self.d + "\n"))
		sdFile.write(str(self.n))
		sdFile.write(str(self.adjArray))
		sdFile.write(str(self.regionsText))

		sdFile.close()
		os.chdir(os.path.expanduser(currDir))
		print  self.name + " saved to " + saveDir

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
