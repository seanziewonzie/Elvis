from sage.all import *
from SaveMessage import *
class SpaceDecomp:
	
	#The user has decided to make a new calculation. They will now be asked if they want to make one from scratch or use a previous situation.	The method will return the resulting space decomposition back to createCalculation.
	def spaceDecompLoadOrNew(self):
		response =raw_input('\nPress l to load a space decomposition. \nPress n to create a new space decomposition. \n')
		while response !='l' and response !='n':
			print('This is not a valid input. Please type l/n: ')
			response =raw_input('\nPress l to load a space decomposition. \nPress n to create a new space decomposition. \n')
		if response == 'l':
			return self.chooseSpaceDecomp()
		if response =='n':
			print('\nYou will now create a new space decomposition.')
			return self.createSpaceDecomp()
	
	def chooseSpaceDecomp(self):
		return 'We have not coded save and write yet'
	
	#This method creates a new space decomposition and returns it.
	def createSpaceDecomp(self):
		d=(int)(input('What is the dimension? '))
		n=(int)(input('How many regions? '))

		regions=[]
		adjArray=[]	

		for i in range(n):
			#Construct a region. Before adding it to regions, check that it is defined by halfspaces of the correct dimension,
			#and that it it does not overlap with previous regions.
			while True:
				hspaces = self.createHalfSpaces(d,i)
				overlap= self.checkOverlap(hspaces,regions,i,d)
				if overlap[0] == True:
					print ('This region overlaps with region ' + str(overlap[1]+1) +'. Try again.')
				else:
					break

			regions.append(hspaces)

			#This will constantly update the adjacency matrix so that two regions are considered adjacent if and only if 
			#their intersection is not subsumed by another intersection
			if i==0:
				adjArray.append([0])
			else:
				self.updateAdjacencyArray(adjArray,regions,i)

		adjGraph = self.makeGraph(adjArray,regions,n)

		spaceDecomp =[d,n,adjGraph]
		
		self.saveSpaceDecomp()
				
		return spaceDecomp


	#This method will get the halspaces that define a region, but it will check that the halfspaces are sensible.
	def createHalfSpaces(self,d,i):
		hspaces=[]
		m=(int)(input('\nHow many halfspaces cut out region '+str(i+1)+'? '))
		for j in range(m):
			while True:
				#Get a halfspace from the user
				if j==0:
					rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'st halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n').split(" ") 
				elif j==1:
					rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'nd halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n').split(" ") 
				elif j==2:
					rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'rd halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n').split(" ") 
				else:
					rawnums = raw_input('\nGive a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'th halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... anxn <= 0 \n').split(" ") 

				#Check if it is the right dimension.
				if len(rawnums) != d+1:
					print('This list is the wrong length. Try again.')
				else:
					break

			#Add the halfspace to the list of halfspaces
			hspace = [float(num) for num in rawnums]
			hspaces.append(hspace)

		hspaces = Polyhedron(ieqs = hspaces)

		return hspaces



	#This method will check if the proposed region overlaps with a previous region
	def checkOverlap(self,hspaces,regions,i,d):
		overlap = [False]
		for j in range(i):
			p = hspaces&regions[j]
			if p.dim()>=d:
				overlap.append(True)
				overlap.append(j)
		return overlap


	def updateAdjacencyArray(self,adjArray,regions,i):
		adjRow=[]
		for j in range(i):
			ijPoly=regions[i]&regions[j]
			if ijPoly.dim()>=0:
				adjacency=1
				for k in range(i):
					if adjArray[j][k]==0:
						adjacency=1
					if adjArray[j][k]==1:
						kjPoly=regions[k]&regions[j]
						if kjPoly&ijPoly==ijPoly:
							adjacency=adjacency*0
						if kjPoly&ijPoly==kjPoly:
							adjacency=adjacency*1
							adjArray[k][j]=0
							adjArray[j][k]=0
						if kjPoly!=ijPoly:
							if kjPoly&ijPoly==ijPoly:
								adjacency=0
								break
							if kjPoly&ijPoly==kjPoly:
								adjArray[k][j]=0
								adjArray[j][k]=0
			else:
				adjacency=0
			
			adjRow.append(adjacency)
			adjArray[j].append(adjacency)


		#The final entry is the adjanceny of i with itself, which we consider to be 0 for simplification 
		adjRow.append(0)
		adjArray.append(adjRow)

	def makeGraph(self,adjArray,regions,n):
		#Make a graph from the adjacency matrix
		adjmatrix=Matrix(adjArray)	
		adjGraph=Graph(adjmatrix)

		#Label the vertices with the appropriate region
		keys=[]
		for i in range(n):
			keys.append(i)
		regionDictionary=dict(zip(keys,regions))
		adjGraph.set_vertices(regionDictionary)

		return adjGraph

	def saveSpaceDecomp(self):
		sm = SaveMessage('space decomposition')
		sm.message()
