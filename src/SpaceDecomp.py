import sys; sys.dont_write_bytecode = True
from sage.all import *
from SaveMessage import *
from ErrorMessage import *
class SpaceDecomp:
	#The user has decided to make a new calculation. They will now be asked if they want to make one from scratch or use a previous situation.	
	#This method will return the resulting space decomposition back to createCalculation.
	def spaceDecompLoadOrNew(self):
		response =raw_input('\nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
		if response == 'q':
			exit()	
		while response!= '1' and response != '2':
			response = raw_input('Please enter 1 or 2. \nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
			if response == 'q':
				exit()	
		if response == '1':
			return self.chooseSpaceDecomp()
		if response =='2':
			print('\nYou will now create a new space decomposition.')
			return self.createSpaceDecomp()
	
	
	def chooseSpaceDecomp(self):
		print('We have not coded save and write yet')
		return []
	

	#This method creates a new space decomposition.
	def createSpaceDecomp(self):
		self.get_d_And_n()


		self.createRegionsAndAdjacency()

		adjGraph = self.makeGraph(adjArray,regions,n)
		spaceDecomp =[d,n,adjGraph]
	
		self.saveSpaceDecomp()		
		return spaceDecomp


	#This method prompts the user for the dimension of space being simulated
	#and the number of polyhedral regions the space has been decomposed into.
	def get_d_And_n(self):
		while True:
			try:
				global d
				d=(int)(input('What is the dimension? '))
			except:
				err=ErrorMessage()
				err.errorMessage()
				continue
			break

		while True:
			try:	
				global n
				n=(int)(input('How many regions? '))
			except:
				err=ErrorMessage()
				err.errorMessage()
				continue
			break


	#This method creates the polyhedral regions and updates a matrix which logs the
	#**relevant** adjacencies
	def createRegionsAndAdjacency(self):
		global regions
		global adjArray
		regions = []
		adjArray = []

		for i in range(n):
			#Construct a region. Before adding it to regions, check that it is defined by halfspaces of the correct dimension,
			#and that it it does not overlap with previous regions.
			while True:
				candidatePoly = self.createCandidate(d,i)
				overlap= self.checkOverlap(candidatePoly,regions,i,d)
				if overlap[0] == True:
					print ('This region overlaps with region ' + str(overlap[1]+1) +'. Try again.')
				else:
					break
			regions.append(candidatePoly)

			#This will constantly update the adjacency matrix so that two regions are considered adjacent if and only if 
			#their intersection is not subsumed by another intersection.
			#If an intersection is subsumed by another intersection, it will be considered as a subcase later when the program
			#considers paths from intersection to intersection. So it may be thrown away to optimize the number of paths
			#handled in the calculation
			if i==0:
				adjArray.append([0])
			else:
				self.updateAdjacencyArray(adjArray,regions,i)


	#This method will get the halspaces that define a region, but it will check that the halfspaces are sensible.
	def createCandidate(self,d,i):
		hspaces=[]
		while True:
			try:
				m=input('\nHow many halfspaces cut out region '+str(i+1)+'? ')
				if m == 'q':
					exit()
				m = (int)(m)
			except:
				err=ErrorMessage()
				err.errorMessage()
				continue
			break

		#Get the list of halfspaces that will together cut out the proposed region i.	
		for j in range(m):
			while True:
				#Get a halfspace from the user
				try:
					if j==0:
						rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'st halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n').split(" ") 
					elif j==1:
						rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'nd halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n').split(" ") 
					elif j==2:
						rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'rd halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n').split(" ") 
					else:
						rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'th halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... anxn <= 0 \n').split(" ") 
					if rawnums == 'q':
						exit()	
					hspace = [float(num) for num in rawnums]
				except:
					err=ErrorMessage()
					err.errorMessage()
					continue

				#Check if it is the right dimension.
				if len(hspace) != d+1:
					print('This list is the wrong length. Try again.')
				else:
					break
			
			#Add the halfspace to the list of halfspaces
			hspaces.append(hspace)

		#Make a polyhedron out of these halfspaces.
		candidatePoly = Polyhedron(ieqs = hspaces)

		return candidatePoly


	#This method will check if the proposed region i overlaps with any previous region.
	def checkOverlap(self,candidatePoly,regions,i,d):
		overlap = [False]
		for j in range(i):
			p = candidatePoly&regions[j]
			if p.dim()>=d:
				overlap.append(True)
				overlap.append(j)
		return overlap


	#This method will update the array of **relevant** adjacencies given this new region i.
	def updateAdjacencyArray(self,adjArray,regions,i):
		adjRow=[]
		for j in range(i):
			#Check if the region intersects with any other region.
			ijPoly=regions[i]&regions[j]
			if ijPoly.dim()>=0:
				#It does intersect with region j. It is possible that we will have to actually consider
				#adjacency as important information.
				adjacency = 1
				#Check all other intersections that region j has.
				for k in range(i):
					if adjArray[j][k]==0:
						#No need to check anything if j and k do not intersect.
						pass
					if adjArray[j][k]==1:
						#j and k do intersect. Does the candidate intersection subsume this intersection?
						#Does this intersection subsume the candidate intersection?
						kjPoly=regions[k]&regions[j]
						if kjPoly == ijPoly:
							#Neither subsumes the other. Both adjacencies may still be necessary to consider.
							pass
						elif kjpoly & ijPoly == ijPoly:
							#The candidate intersection is subsumed.
							adjacency = 0
							break
						else:
							#The candidate intersection subsumes the jk intersection. Stop considering the jk
							#intersection, and continue to check with all other intersections that involve
							#region j.
							adjArray[j][k]=0
							adjarray[k][j]=0
			#If they do not intersect, they are not adjacent in the first place.
			else:
				adjacency=0
			
			#Update the row to indicate whether or not, for now, we are considering the ij adjacency
			#as important.
			adjRow.append(adjacency)
			adjArray[j].append(adjacency)


		#The final entry is the adjanceny of i with itself, which we consider to be 0 for simplification 
		adjRow.append(0)

		#Update the adjacency matrix
		adjArray.append(adjRow)


	#This method returns takes the adjacency information about the regions and returns a properly labeled
	#graph.
	def makeGraph(self,adjArray,regions,n):
		#Make a graph from the adjacency matrix.
		adjmatrix=Matrix(adjArray)	
		adjGraph=Graph(adjmatrix)

		#Label the vertices with the appropriate region.
		keys=[]
		for i in range(n):
			keys.append(i)
		regionDictionary=dict(zip(keys,regions))
		adjGraph.set_vertices(regionDictionary)

		return adjGraph


	#Give an option to save this new space decomposition as a folder within the "Situations" folder.
	def saveSpaceDecomp(self):
		sm = SaveMessage('space decomposition')
		sm.message()