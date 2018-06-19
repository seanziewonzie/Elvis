import sys; sys.dont_write_bytecode = True
from sage.all import *
from Situation import *
from StartAndEnd import *
from SaveMessage import *
class Calculation:
	#The user will be asked if they want to utilize a calculation which has previously been made or if they want to make a new one.	
	def calculationLoadOrNew(self):
		response =raw_input('\nPress 1 to load a calculation. \nPress 2 to create a new calculation. \n')
		if response == 'q':
			raise SystemExit
		while response != '1' and response != '2':
			response =raw_input('Please enter 1 or 2. \nPress 1 to load a calculation. \nPress 2 to create a new calculation. \n')
			if response == 'q':
				raise SystemExit
		if response == '1':
			return self.chooseSpaceDecomp()
		if response =='2':
			print('\nYou will now create a new calculation.')
			return self.createCalculation()


	def handleCalculation(self,calculation):
		print('We have not coded any options to handle calculations')

		#Here they will have the option of deleting calculations, getting a text description of a calculation, 
		#plotting 2-D and maybe 3-D calculations, merging calculations, renaming calculations, and maybe more.

		response = raw_input('\nEnter 1 to perform another action with this calculation. \nEnter 2 to get go back to the beginning. \n')
		if response == 'q':
			raise SystemExit
		return response

	
	def chooseCalculation(self):
		#We let them load a calculation from the Calculations folder, and see which Calculations are in the Calculation folder
		#calculation = whatever the user chooses
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
		
		#With these three specifications, the time function is well defined.
		problem = [situation,startAndEnd]
		calculation = self.Optimization(problem)
		
		self.saveCalculation()
			
		return calculation


	#Given a problem, this method will find the path in the situation from the start point to the endpoint which
	#minimizes the time function.
	def Optimization(self,problem):
		#This classifies and enumerates all paths in our space decomposition from the start point to the end point
		#In fact, it only classifies the ones worthy of consideration.
		paths = problem[0][0][2].all_paths(problem[1][0][1],problem[1][1][1])
		print paths
		p = len(paths)
		if p == 0:
			print('\nThere are no paths between the starting point and the ending point.\n')
			return []
		else:
			optimalPaths = []
			optimalTimes = []
			for k in range(p):
				path = paths[k]
				l = len(path)
				#declare the d*(p+1) variables/degrees of freedom which represent the coordinates of the points in
				#the intersections of the polyhedra in the path.
				xs = [var('x_'+str(i)+"_"+str(j)) for i in range(l+1) for j in range(d)]
				#T is the function to minimize
				T = 0
				for i in range(l):
					#The following loop builds an expression for the distance between one chosen point and the next.
					sqDist=0
					for j in range(d):
						sqDist = sqDist[i] + (xs[i+1][j]-xs[i][j])^2
					#The time that one piece of the path contributes (depends on distance and velocity).
					t = (1/problem[0][1][i])*sqrt(sqDist)
					#Add it to the total time function
					T = T + t
				constraints=[]
				#Constrain the first d variables to be the correspond to the coordinates of the starting point.
				for j in range(d):
					constraints.append(xs[0][j] - problem[1][0][0][j])
					constraints.append(problem[1][0][0][j] - xs[0][j])
				#Constrain the last d variables to be the correspond to the coordinates of the ending point.
				for j in range(d):
					constraints.append(xs[l][j] - problem[1][1][0][j])
					constraints.append(problem[1][1][0][j] - xs[l][j])
				#Constain the i-th d-tuple of variables so that they together represent a point which is contained in
				#the intersection of the i-1-th and i-th polyhedron in the path.
				if l >= 2:
					for i in range(1,l): 
						#Get the intersection of polyhedron which this i-th point must lie in.
						exitPoly = problem[0][0][2].get_vertex[i-1]
						enterPoly = problem[0][0][2].get_vertex[i]
						intersection = exitPoly&enterPoly
						#Get the inequalities which define this polyhedron, and apply them to the i-th point.
						constraintsForPoint = getConstraintsForPoint(intersection,xs,i)
						#Add this constraint to the running list of constraints.
						constraints = constraints + constraintsForPoint
				#Get an initial point to do the optimization from.
				initialPoint = []
				for j in range(d):
					initialPoint.append(problem[1][0][0][j])
				for i in range(l):
					exitPoly = problem[0][0][2].get_vertex[i-1]
					enterPoly = problem[0][0][2].get_vertex[i]
					intersection =exitPoly&enterPoly
					referencePoint = intersection.representative_point()
					for j in range(d):
						intialPoint.append(referencePoint[j])
				for j in range(d):
					initialPoint.append(problem[1][1][0][j])
				optimalInput = minimize_constrained(T,constraints,initialPoint)
				optimalPath = []
				for i in range(l+1):
					optimalPath.append(optimalInput[d*i:d*(i+1)])
				optimalPaths.append(optimalPath)
				inputArray=[]
				#Figure out how to actually plug the minimal point into the function
				optimalTime = T.subs(x[i][j]=optimalPath[i][j])
				optimalTimes.append(optimalTime)
			bestTime = optimalTimes.min()
			bestPath = optimalTimes.argmin()
			best = [bestTime,bestPath]
			return [best,problem]




	#Get the numerical expressions determined by the polyhedral interface this point must lie in to get the constraint.
	def getConstraintsForPoint(self,intersection,xs,i):	
		#Get a representation of the inequalities which bound this polyhedron.			
		a = intersection.Hrepresentation()
		length = len(a)
		array = []
		for i in range(length):
			#The Hrepresentation is a weird object that is an array of some sort of pickled strings describing
			#the hspaces in prose, rather than just as numbers. This will unpack it into an easy-to-use array.
			string = str(a[i])
			b = string.split(" ")
			b = b[2:-2]
			b[0] = b[0][1:-1]
			for j in range(d-1):
				b[j+1] = b[j+1][:-1]
			b.remove('x')
			#With this new array, generate an expression which would represent what exactly is >=0 in this inequality.
			constraint = 0
			for j in range(d):
				constaint = constraint + float(b[j])*xs[i][j]
			if b[d+1] == '+':
				constraint = constraint + float(b[d+1])
			if b[d-1] == '-':
				constraint = constraint - float(b[d+1])
			#If it is an equality, break it up into two over-determined inequalities. Add the inequalit(y/ies) to the array
			#of constraints.
			if "equation" in str(a[i]):
				array.append(constraint)
				negConstraint = (-1)*constraint
				array.append(negConstraint)
			if "inequality" in str(a[i]):
				array.append(constraint)
		return array
				




	def saveCalculation(self):
		sm = SaveMessage('calculation')
		sm.message()
