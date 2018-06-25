import sys; sys.dont_write_bytecode = True
from sage.all import *
import SpaceDecomp as SpaceDecomp
import Velocities as Velocities
import Message
import numpy as np
import os
import errno
import subprocess
import re
import platform
import ast
class Calculation:
	def __init__(self):
		self.name = ""
		self.sit = None
		self.startCoords =[]
		self.startRegion = 0
		self.endCoords = []
		self.endRegion = None
		self.bestTime = None
		self.bestPath = None


	#The user will be asked if they want to utilize a calculation which has previously been made or if they want to make a new one.	
	def calculationLoadOrNew(self):
		while True:
			response = Message.getResponse('\nPress 1 to load a calculation. \nPress 2 to create a new calculation. \n')
			if response != '1' and response != '2':
				print 'Please enter 1 or 2.'
				continue
			break
		if response == '1':
			self.chooseCalculation()
		if response =='2':
			self.createCalculation()


	#With calculation in hand, the user will have the option to do something with it.
	#Currently there are no options.
	#Potential actions: plotting, merging two calculations together to plot them together, deleting, renaming.		
	def handleCalculation(self):
		while True:
			response = Message.getResponse('\nEnter 1 to perform another action with this calculation. \nEnter anything else to get go back to the beginning. \n')
			if response == 1:
				print '\nWe have not coded any options to handle calculations'
				continue
			break

	
	#We let the user load a calculation from the Calculations folder (and to help them, they can see which calculations are in the Calculations folder).
	def chooseCalculation(self):
		#Show them which calculations exist.
		os.chdir(os.path.expanduser("~/Documents/ElvisFiles/Calculations"))
		print "\nYour saved calculations"
		subprocess.call("ls")

		#Let the user choose the calculation. Keep asking until it is actually a calculation which exists.
		while(True):
			chosenCalculation = Message.getResponse("\nSelect a calculation (case sensitive): ")
			try:
				os.chdir(os.path.expanduser(chosenCalculation))
				break
			except:
				if OSError.errno == errno.ENOENT:
					print "---That calculation does not exist, retry---"
				else:
					Message.errorMessage()

		#Populate all the variables of this calculation and all the fields of all the classes which are variables in this calculation.
		self.name = chosenCalculation

		self.sit = Situation()
		self.sit.sd = SpaceDecomp.SpaceDecomp()
		self.sit.vel = Velocities.Velocities(self.sit.sd)

		with open("Space_Decomp_Info.txt","r") as file:
			contentSD = file.readlines()
		contentSD = [x.strip() for x in contentSD]
		self.sit.sd.name = contentSD[0]
		self.sit.sd.d = (int)(contentSD[1])
		self.sit.sd.n = (int)(contentSD[2])
		self.sit.sd.adjArray = ast.literal_eval(contentSD[3])
		self.sit.sd.regionsText = ast.literal_eval(contentSD[4])
		self.sit.sd.regionsPoly = [Polyhedron(ieqs = x) for x in self.sit.sd.regionsText]
		self.sit.sd.makeGraph()

		with open("Velocities_Info.txt","r") as file:
			contentVEL = file.readlines()
		contentVEL = [x.strip() for x in contentVEL]
		self.sit.vel.name = contentVEL[0]
		self.sit.vel.velocities = ast.literal_eval(contentVEL[1])

		with open("Start_And_End_Info.txt","r") as file:
			contentSAE = file.readlines()
		contentSAE = [x.strip() for x in contentSAE]
		self.startCoords =ast.literal_eval(contentSAE[0])
		self.startRegion = ast.literal_eval(contentSAE[1])
		self.endCoords = ast.literal_eval(contentSAE[2])
		self.endRegion = ast.literal_eval(contentSAE[3])

		with open("Solution_Info.txt","r") as file:
			contentSOL = file.readlines()
		contentSOL = [x.strip() for x in contentSOL]

		#Perhaps this calculation had no solution (because the starting point and the ending points were disconnected).
		#Then the best path and the best time would not have been saved as numerical information, but instead as messages
		#of 'no solution'. Assign the values accordingly.
		if contentSOL[0] == 'There is no way to get from the starting point to the ending point in this situation.':
			self.bestTime = 'There is no way to get from the starting point to the ending point in this situation.'
		else:
			self.bestTime =ast.literal_eval(contentSOL[0])
		if contentSOL[1] == 'There is no way to get from the starting point to the ending point in this situation.':
			self.bestTime = 'There is no way to get from the starting point to the ending point in this situation.'
		else:
			self.bestPath = ast.literal_eval(contentSOL[1])


	#The user will create a calculation from a situation and a choice of start and end points.
	def createCalculation(self):
		#Get the situation.
		self.sit = Situation()
		self.sit.situationLoadOrNew()

		#Get the start and end points within this space decomposition.
		self.startCoords,self.startRegion=self.pointInfo("start")
		self.endCoords,self.endRegion =self.pointInfo("end")
		
		#With these variables assigned, the time function can be well defined, so do the actual optimization
		#to get the solution.
		self.Optimization()

		self.saveCalculation()


	#This method gets the user to input the start coordinates or the end coordinates, depending on the string.
	#The method also determines which region the starting and ending points lie in.
	def pointInfo(self,string):
		#This will prompt the user to input (valid) coordinates.
		while True:
			#Get the input, and keep trying until they are actually numbers.
			while True:
				rawCoords = Message.getResponse('\nWhat are the coordinates of the ' +string +'ing point? \n').split(" ")
				try:
					coords = [float(num) for num in rawCoords]
				except:
					Message.errorMessage()
					continue
				break
			
			#This point will have to prove that it is sensible. If not, 
			#the user will be asked to input again.
			contained = 0
			
			#If it is  not the right dimension, ask the user for coordinates again.
			if len(coords)!=self.sit.sd.d:
				print('The '+ string +'ing point should be specified by ' + str(self.sit.sd.d) + ' coordinates. Try again. ')
				continue
			
			#Get the first region the point is contained in. 
			for i in  range(self.sit.sd.n):
				P = self.sit.sd.adjGraph.get_vertex(i)
				if P.contains(coords):
					contained = 1
					region = i 
					break
			
			#If the point was actually not contained in any region, ask the user for coordinates again.
			if contained ==1:
				#This is a sensible point. 
				break
			else:
				print('This point is not contained in any region. Try again. ')

		return coords,region


	#Given a problem, this method will find the path in the situation from the start point to the endpoint which
	#minimizes the time function, and it will find the time output of that path.
	def Optimization(self):
		#This classifies and enumerates all paths in our space decomposition from the start point to the end point
		#In fact, it only classifies the ones worthy of consideration (this is why we reduced the adjacency array).
		paths = self.sit.sd.adjGraph.all_paths(self.startRegion,self.endRegion)
		p = len(paths)

		#If p==0, there are no paths at all. Let bestTime and bestPath be strings which state this.
		if p == 0:
			print('\nThere are no paths between the starting point and the ending point.\n')
			self.bestTime = 'There is no way to get from the starting point to the ending point in this situation.'
			self.bestPath = 'There is no way to get from the starting point to the ending point in this siutation.'
		else:
			#This array will store the optimal path for each class of paths.
			optimalPaths = []

			#This array will store the optimal time for each class of paths.
			optimalTimes = []

			#For each particular class of paths, find the optimal path among them.
			for k in range(p):
				path = paths[k]
				l = len(path)
				
				#All relevant mathematical objects in minimzed_constrained-- the function, the constraints, the initial point --
				#will be written with respect to d*(l-1) variables. They will be indexed 'x's. Slicing this list of d*(l-1) variables
				#into pieces of length d, every piece represents a turning point of the path.

				#T is the function to minimize. Create it and turn it into a lambda function.
				T=self.functionToMinimize(l)
				S = lambda x: eval(T)

				#Get the constraints this function must be minimized over. We only care about points which are in the 
				#correct interfaces. Turn them into lambda functions.
				constraints=self.getConstraints(l)
				lambdas_list =[]
				for i in range(len(constraints)):
					lambdas_list.append(self.build_lambdas(constraints,i))

				#Get an initial point to do the optimization from.
				initialPoint = self.generateIntialPoint(l)

				#This actually calculates where the function is minimized
				optimalInput = minimize_constrained(S,lambdas_list,initialPoint)

				#Get the optimal time by actually plugging the optimal path into the time function. Now the 2D array of
				#input numbers will take the role of the 2D array of variables, and the functionToMinimize method will 
				#return a value, not a symbolic function
				optimalTime = S(optimalInput)

				#This packs the path into a more readable 2D array rather than one long array. Each row is a turning point of the path.
				optimalPath = []
				for i in range(l+1):
					optimalPath.append(optimalInput[self.sit.sd.d*i:self.sit.sd.d*(i+1)])
				
				#Add the optimalPath to the running list of optimal paths.
				optimalPaths.append(optimalPath)

				#Add the optimalTime to the running list of optimal times.
				optimalTimes.append(optimalTime)

			#Get the best time from the best times of all classes of paths, and the path which causes it.	
			self.bestTime = np.min(optimalTimes)
			bestPathNum = np.argmin(optimalTimes)
			self.bestPath = optimalPaths[bestPathNum]

			#Let the user see information about this solution.
			self.printSolution()


	#This function will build a mathematical expression of the time a path from the starting point to the ending point takes 
	#in the situation.
	def functionToMinimize(self,l):
		T = '0'
		for i in range(l):
			#The following loop builds an expression for the distance between one chosen point and the next.
			sqDist='0'
			for j in range(self.sit.sd.d):
				sqDist = sqDist + '+(x[' +str(self.sit.sd.d*(i+1)+j)+ ']-x[' +str(self.sit.sd.d*i+j)+ '])**2'
			
			#The time that one piece of the path contributes (depends on distance and velocity).
			t = '(1.0/' +str(self.sit.vel.velocities[i])+ ')*sqrt(' + sqDist + ')'
			
			#Add it to the total time function
			T = T+ '+' +t
		return T


	#This will generate an array of "expressions" which correspond to inequalities involving the variables x_i_j. These inequalities
	#will force the function to only be minimized over the class of paths which go between the correct interfaces ("correct" meaning
	#corresponding to the class of paths under consideration).
	#Unfortunately, the minimized_constrained method only accepts lambda functions, and making lambda functions out of functions is 
	#difficult with a dynamic list of variables. So I have made a really hacky work-around:
	#Let each expression be a **string**. Then the lambda function will just be to apply eval to the string.
	def getConstraints(self,l):
		constraints=[]
		#Constrain the first d variables to be the correspond to the coordinates of the starting point. Cast the constraint as
		#a function expression.
		for j in range(self.sit.sd.d):
			#Constraints are inequalities. To force an equality -- say, x = 1 -- we must use two inequalities:
			# x <=1 and x>=1.
			constraints.append('x['+str(j)+'] -' + str(self.startCoords[j]))
			constraints.append(str(self.startCoords[j]) +' - x['+str(j)+']')

		#Constain the i-th d-tuple of variables so that they together represent a point which is contained in
		#the intersection of the (i-1)-th and i-th polyhedron in the path.
		if l >= 2:
			for i in range(1,l): 
				#Get the intersection of polyhedron which this i-th point must lie in.
				exitPolyText = self.sit.sd.regionsText[i-1]
				enterPolyText = self.sit.sd.regionsText[i]
				intersectionText = exitPolyText+enterPolyText
				for ineq in intersectionText:
					constraint = str(ineq[0])
					for j in range(self.sit.sd.d):
						constraint = constraint + '+' + str(ineq[j+1]) + "*x[" +str(i*self.sit.sd.d+j) + "]"
					constraints.append(constraint)
		
		#Constrain the last d variables to be the correspond to the coordinates of the ending point. Cast the constraint as
		#a function expression.
		for j in range(self.sit.sd.d):
			#Constraints are inequalities. To force an equality -- say, x = 1 -- we must use two inequalities:
			# x <=1 and x>=1.
			constraints.append('x['+str(l*self.sit.sd.d+j)+'] -' + str(self.endCoords[j]))
			constraints.append(str(self.endCoords[j]) +'- x['+str(l*self.sit.sd.d+j)+']')


	
		return constraints
				
	
	#Convert constraints into lambdas. Since the constraints have been created as strings, we must evaluate them.
	def build_lambdas(self,constraints,i):
		return lambda x: eval(constraints[i])


	#This will generate an inital point to begin the optimization process.			
	def generateIntialPoint(self,l):
		initialPoint = []
		
		#The first d coordinates must correspond to the starting point
		for j in range(self.sit.sd.d):
			initialPoint.append(self.startCoords[j])
		
		if l>=2:
			#The middle d-tuples must correspond to points which are part of the corresponsing interfaces.
			#This is what representative_point accomplishes.
			for i in range(1,l):
				exitPoly = self.sit.sd.adjGraph.get_vertex(i-1)
				enterPoly = self.sit.sd.adjGraph.get_vertex(i)
				intersection =exitPoly&enterPoly
				referencePoint = intersection.representative_point()

				#We have the representative point. Populate the next d coordinates of the inital input point with
				#the coordinates of the representative point.
				for j in range(self.sit.sd.d):
					initialPoint.append(referencePoint[j])
		
		#The final d coordinates must correspond to the ending point
		for j in range(self.sit.sd.d):
			initialPoint.append(self.endCoords[j])
		
		return initialPoint


	#Print the best path and the best time.
	def printSolution(self):
		print('\nThe best time is: '+ str(self.bestTime) +'\n')

		length= len(self.bestPath)
		print('The best path is as follows:')
		for i in range(length):
			if i== 0:
				print('Start at')
			elif i== length:
				print('and end at')
			else:
				print('and head to')
			print self.bestPath[i]


	#This method gives the user the option to save the calculation and -- if they say yes -- saves the calculation as
	#a folder in the Calculations folder, with text files describing the relevant details.
	def saveCalculation(self):
		save = Message.getResponse("Save this calculation(y/n): ")
		while save != "y" and save != "n":
			save = Message.getResponse("Error, type either y or n, retry: ")

		#They decided to save:
		if save == "y":
			#Mark the current directory, so we can return back to it after all of this writing.
			currDir = os.getcwd()
			
			#They will keep giving a name to the calculation until it both makes sense and is not already the name
			#of another saved calculation.
			while True:
				self.name = Message.getResponse("Name your calculation: ")
				os.chdir(os.path.expanduser('~/Documents/ElvisFiles/Calculations'))
				try:
					os.makedirs(self.name)
					os.chdir(os.path.expanduser(self.name))
					saveDir = os.getcwd()
				except:
					if OSError.errno != errno.EEXIST:
						Message.errorMessage()
					else:	
						print "ERROR... Already a saved calculation. \n"
					continue
				break


			#Write all of the relevant details of this calculation to text files
			sdFile = open("Space_Decomp_Info.txt","w+")
			sdFile.write(self.sit.sd.name + "\n")
			sdFile.write(str(self.sit.sd.d) + "\n")
			sdFile.write(str(self.sit.sd.n )+ "\n")
			sdFile.write(str(self.sit.sd.adjArray) + "\n")
			sdFile.write(str(self.sit.sd.regionsText) + "\n")
			sdFile.close()

			velFile = open("Velocities_Info.txt","w+")
			velFile.write(str(self.sit.vel.name)  + "\n")
			velFile.write(str(self.sit.vel.velocities))
			velFile.close()

			startAndEndFile = open("Start_And_End_Info.txt","w+")
			startAndEndFile.write(str(self.startCoords) + "\n")
			startAndEndFile.write(str(self.startRegion) + "\n")
			startAndEndFile.write(str(self.endCoords) + "\n")
			startAndEndFile.write(str(self.endRegion) + "\n")
			startAndEndFile.close()

			solutionFile = open("Solution_Info.txt","w+")
			solutionFile.write(str(self.bestTime) + "\n")
			solutionFile.write(str(self.bestPath) + "\n")
			solutionFile.close()

			#Go back to the directory the user was in before this writing process.
			os.chdir(os.path.expanduser(currDir))

			#A confirmation message for the user.
			print  self.name + " saved to " + saveDir


###############################################################################################################################
###############################################################################################################################

###############################################################################################################################
###############################################################################################################################
class Situation:
	def __init__(self):
		self.sd = None
		self.vel = None


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
			#Initialize a space decomposition. Let it be the space decomposition of the user's choice.
			self.sd=SpaceDecomp.SpaceDecomp()
			self.sd.chooseSpaceDecomp()
			
			#Initialize a velocity set for this space decomposition.
			self.vel = Velocities.Velocities(self.sd)

			#Check that this space decomposition even has velocity sets.
			list_dir = os.listdir(os.path.expanduser('~/Documents/ElvisFiles/Situations/'+self.sd.name+'/Velocities/'))
			count = 0
			for file in list_dir:
				count += 1

 			#If there are no velocity sets, the user can make one, or choose a different space decomposition (starting this grand while loop over).
			if count == 0:
				print 'There are no velocity sets associated to this space decomposition. \n'
				while True:
					response = Message.getResponse('Enter 1 to create a new velocity set for this space decomposition. \nEnter 2 to choose a different space decomposition.\n')
					if response != '1' and response !='2':
						print 'Please enter 1 or 2.'
						continue
					break
				if response =='1':
					self.vel.createVelocities()
				if response =='2':
					continue				
			
			#If there are velocity sets, proceed as normal: let the velocity set be the velocity set of the user's choice.
			else:
				self.vel.chooseVelocities()
			break
		

	#This creates a situation, which is a space decomposition together with an associated velocity set.
	def createSituation(self):
		#Get (by loading or creating) a space decomposition.
		self.sd=SpaceDecomp.SpaceDecomp()
		self.sd.spaceDecompLoadOrNew()
		
		#Make a velocity set for this space decomposition.
		self.vel = Velocities.Velocities(self.sd)
		self.vel.createVelocities()
		
	
	#Here a user chooses to view or edit their chosen situation, or go back to the beginning of the program.
	def viewOrEditSituation(self):
		while True:
			response = Message.getResponse('\nEnter 1 to view information about this situation. \nEnter 2 to edit this situation. \nEnter anything else to go back to the beginning. \n')
			if response == 1:
				viewSituation()
				continue
			if response == 2:
				editSituation()
				continue
			break


	#Here a user will be able to view a saved situation in the Situation folder. This has not yet been coded.
	def viewSituation(self):
		print('There is currently no way to view information about saved situations. ')
		return []
		

	#Here a user will be able to edit a saved situation in the Situation folder. This has not yet been coded.	
	def editSituation(self):
		print('There is currently no way to edit saved situations. ')
		return []