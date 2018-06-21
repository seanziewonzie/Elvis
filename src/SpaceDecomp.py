import sys; sys.dont_write_bytecode = True
import Inflect
ordinator=Inflect.engine()
from sage.all import *
from SaveMessage import *
from ErrorMessage import *
import os
import errno
import subprocess
import re
import platform


class SpaceDecomp:

	#The user has decided to make a new calculation. They will now be asked if they want to make one from scratch or use a previous situation.	
	#This method will return the resulting space decomposition back to createCalculation.
	def __init__(self):
		self.d = 0
		self.n = 0
		self.adjArray = []
		self.name = ""
		self.loadedArrayString = ""

	def spaceDecompLoadOrNew(self):
		response =raw_input('\nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
		if response == 'q':
			raise SystemExit	
		while response!= '1' and response != '2':
			response = raw_input('Please enter 1 or 2. \nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
			if response == 'q':
				raise SystemExit	
		if response == '1':
			return self.chooseSpaceDecomp()
		if response =='2':
			print('\nYou will now create a new space decomposition.')
			return self.createSpaceDecomp()

	#loads a pre-existing Space Decompositons and prints relevant info to user
	def chooseSpaceDecomp(self):

		os.chdir(os.path.expanduser("~/Documents/Elvis/Situations"))
		print "\nYour saved Space Decompositions\n"
		if platform.system() == "Linux":
			subprocess.call("ls")
		elif platform.system() == "Windows":
			subprocess.call("dir /s")
		while(True):
			try:
				chosenDecomp = raw_input("Select a Space Decomposition (case sensitive): ")
				os.chdir(os.path.expanduser(chosenDecomp))
				break
			except OSError as e:
				if e.errno == errno.ENOENT:
					print "---That file does not exist, retry---"
	
		chosenDecompFile = open("Space_Decomp_Info.txt","r")

		global counter
		counter = 1
		arrayString = ""
		for line in chosenDecompFile:
			if counter == 1:
				self.n = int(re.search(r'\d+',line).group())
			elif counter == 2:
				self.d = int(re.search(r'\d+',line).group())
			elif counter > 3:
				arrayString = line + arrayString
			counter = counter + 1

		chosenDecompFile.close()
		self.loadedArrayString = arrayString

		print "regions --> " + str(self.n)
		print "dims --> " + str(self.d)
		print "adjanceny --> " + self.loadedArrayString
	#This method creates a new space decomposition.
	def createSpaceDecomp(self):
		self.getDimensionsAndRegions()
		self.createRegionsAndAdjacency()

		adjGraph = self.makeGraph()
		self.spaceDecomp =[self.d,self.n,adjGraph]
	

		save = raw_input("Save this Space Decomp(y/n): ")
		while(True):
			if save == "y":
				self.saveSpaceDecomp(self.spaceDecomp)
				break
			elif save != "y" or save != "n":
				save = raw_input("Error, type either y or n, retry: ")		


		return self.spaceDecomp

	#This method prompts the user for the dimension of space being simulated
	#and the number of polyhedral regions the space has been decomposed into.
	def getDimensionsAndRegions(self):
		while True:
			try:
				#global d
				raw=raw_input('What is the dimension? ')	
				self.d=int(raw)
			except:
				if raw == 'q':
					raise SystemExit
				err=ErrorMessage()
				err.errorMessage()
				continue
			break

		while True:
			try:	
				#global n
				raw=raw_input('How many regions? ')
				self.n = (int)(raw)
			except:
				if raw == 'q':
					raise SystemExit	
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

		for i in range(self.n):
			#Construct a region. Before adding it to regions, check that it is defined by halfspaces of the correct dimension,
			#and that it it does not overlap with previous regions.
			while True:
				candidatePoly = self.createCandidate(i)
				overlap= self.checkOverlap(candidatePoly,i)
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
				self.updateAdjacencyArray(i)
			for j in range(i+1):
				print adjArray[j]


	#This method will get the halspaces that define a region, but it will check that the halfspaces are sensible.
	def createCandidate(self,i):
		hSpaces=[]
		while True:
			try:
				raw=raw_input('\nHow many halfspaces cut out region '+str(i+1)+'? ')
				m = (int)(raw)
			except:
				if raw == 'q':
					raise SystemExit
				err=ErrorMessage()
				err.errorMessage()
				continue
			break

		#Get the list of halfspaces that will together cut out the proposed region i.	
		for j in range(m):
			while True:
				#Get a halfspace from the user
				try:
					rawNums = raw_input('\nGive a list of ' + str(self.d + 1) + ' numbers to indicate the ' +ordinator.ordinal(j+1)+ ' halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponsing to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n')
					splitNums = rawNums.split(" ")
					hSpace = [float(num) for num in splitNums]
				except:
					if rawNums == 'q':
						raise SystemExit
					err=ErrorMessage()
					err.errorMessage()
					continue

				#Check if it is the right dimension.
				if len(hSpace) != self.d+1:
					print('This list is the wrong length. Try again.')
				else:
					break
			
			#Add the halfspace to the list of halfspaces
			hSpaces.append(hSpace)

		#Make a polyhedron out of these halfspaces.
		candidatePoly = Polyhedron(ieqs = hSpaces)

		return candidatePoly


	#This method will check if the proposed region i overlaps with any previous region.
	def checkOverlap(self,candidatePoly,i):
		overlap = [False]
		for j in range(i):
			p = candidatePoly&regions[j]
			if p.dim()>=self.d:
				overlap.append(True)
				overlap.append(j)
		return overlap


	#This method will update the array of **relevant** adjacencies given this new region i.
	def updateAdjacencyArray(self,i):
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
						elif kjPoly & ijPoly == ijPoly:
							#The candidate intersection is subsumed.
							adjacency = 0
							break
						elif kjPoly & ijPoly == kjPoly:
							#The candidate intersection subsumes the jk intersection. Stop considering the jk
							#intersection, and continue to check with all other intersections that involve
							#region j.
							adjArray[j][k]=0
							adjArray[k][j]=0
						else:
							#Their symmetric difference is nonempty. No adjacencies are thrown away.
							pass
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
		self.adjArray = adjArray


	#This method returns takes the adjacency information about the regions and returns a properly labeled
	#graph.
	def makeGraph(self):
		#Make a graph from the adjacency matrix.
		adjmatrix=Matrix(self.adjArray)	
		adjGraph=Graph(adjmatrix)

		#Label the vertices with the appropriate region.
		keys=[]
		for i in range(self.n):
			keys.append(i)
		regionDictionary=dict(zip(keys,regions))
		adjGraph.set_vertices(regionDictionary)

		return adjGraph

	#return objects regions
	def getRegions(self):
		return self.n

	#return objects dimensions
	def getDimensions(self):
		return self.d

	#return objects adjanceny graph
	def getAdjGraph(self):
		return self.adjGraph

	#Give an option to save this new space decomposition as a folder within the "Situations" folder.
	def saveSpaceDecomp(self,spaceDecomp):
		#Save the Space Decomp to the file structure created when setup.py is run
		self.name = raw_input("Name your Space Decomp: ")
		currDir = os.getcwd()
		os.chdir(os.path.expanduser('~/Documents/Elvis/Situations'))
		try:
			os.makedirs(self.name)
			os.chdir(os.path.expanduser(self.name))
			saveDir = os.getcwd()
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
			else:	
				self.name = raw_input("ERROR... Already a saved Decomposition, try again: \n") 
				os.makedirs(self.name)
				os.chdir(os.path.expanduser(self.name))
				saveDir = os.getcwd()
		
		sdFile = open("Space_Decomp_Info.txt","w+")
		sdFile.write("Number_of_Dimensions: " + str(self.spaceDecomp[0]) + "\n")
		sdFile.write("Number_of_Regions: " + str(self.spaceDecomp[1]) + "\n")
		sdFile.write("Adjanceny Graph: \n")

		textGraph = self.adjArray
		for j in range(self.n):
			sdFile.write(str(textGraph[j]) + "\n")
		sdFile.close()

		os.chdir(os.path.expanduser(currDir))
		print  self.name + " saved to " + saveDir

	
