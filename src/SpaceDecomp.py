import sys; sys.dont_write_bytecode = True
import Inflect
ordinator=Inflect.engine()
from sage.all import *
import Message
import os
import errno
import subprocess
import re
import platform
import ast
class SpaceDecomp:
	def __init__(self):
		self.name = ""
		self.d = 0
		self.n = 0
		self.regionsText = []
		self.regionsPoly = []
		self.adjArray = []
		self.adjGraph = None



	#The user has decided to make a new calculation. They will now be asked if they want to make one from scratch or use a previous situation.	
	#This method will return the resulting space decomposition back to createCalculation.
	def spaceDecompLoadOrNew(self):
		response = Message.getResponse('\nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
		while response!= '1' and response != '2':
			response = Message.getResponse('Please enter 1 or 2. \nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
		if response == '1':
			self.chooseSpaceDecomp()
		if response =='2':
			print('\nYou will now create a new space decomposition.')
			self.createSpaceDecomp()



	#This method loads a pre-existing Space Decompositons and prints relevant info to user.
	def chooseSpaceDecomp(self):
		os.chdir(os.path.expanduser("~/Documents/Elvis/Situations"))
		print "\nYour saved space decompositions\n"
		if platform.system() == "Linux":
			subprocess.call("ls")
		elif platform.system() == "Windows":
			subprocess.call("dir /s")

		while(True):
			chosenDecomp = Message.getResponse("Select a space decomposition (case sensitive): ")
			try:
				os.chdir(os.path.expanduser(chosenDecomp))
				break
			except OSError as e:
				if e.errno == errno.ENOENT:
					print "---That space decomposition does not exist, retry---"
				else:
					Message.errorMessage()

		self.name = chosenDecomp
		with open("Space_Decomp_Info.txt","r") as file:
			content = file.readlines()
		content = [x.strip() for x in content]
		self.name = content[0]
		self.d = (int)(content[1])
		self.n = (int)(content[2])
		self.adjArray = ast.literal_eval(content[3])
		self.regionsText = ast.literal_eval(content[4])
		self.regionsPoly = [Polyhedron(ieqs = x) for x in self.regionsText]
		self.makeGraph()



	#This method creates a new space decomposition.
	def createSpaceDecomp(self):
		self.getDimensionsAndRegions()
		self.createRegionsAndAdjacency()
		self.makeGraph()


		save = Message.getResponse("Save this space decomposition(y/n): ")
		while save != "y" and save != "n":
			save = Message.getResponse("Error, type either y or n, retry: ")
		if save == "y":
			self.saveSpaceDecomp()
				


	#This method prompts the user for the dimension of space being simulated
	#and the number of polyhedral regions the space has been decomposed into.
	def getDimensionsAndRegions(self):
		while True:
			raw=Message.getResponse('What is the dimension? ')
			try:	
				self.d=int(raw)
			except:
				if raw == 'q':
					raise SystemExit
				Message.errorMessage()
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
				Message.errorMessage()
				continue
			break


	#This method creates the polyhedral regions and updates a matrix which logs the
	#**relevant** adjacencies
	def createRegionsAndAdjacency(self):
		for i in range(self.n):
			#Construct a region. Before adding it to regions, check that it is defined by halfspaces of the correct dimension,
			#and that it it does not overlap with previous regions.
			while True:
				candidateHSpaces = self.createCandidate(i)
				#Make a polyhedron out of these halfspaces.
				candidatePoly = Polyhedron(ieqs = candidateHSpaces)
				overlap= self.checkOverlap(candidatePoly,i)
				if overlap[0] == True:
					print ('This region overlaps with region ' + str(overlap[1]+1) +'. Try again.')
				else:
					break
			self.regionsText.append(candidateHSpaces)
			self.regionsPoly.append(candidatePoly)

			#This will constantly update the adjacency matrix so that two regions are considered adjacent if and only if 
			#their intersection is not subsumed by another intersection.
			#If an intersection is subsumed by another intersection, it will be considered as a subcase later when the program
			#considers paths from intersection to intersection. So it may be thrown away to optimize the number of paths
			#handled in the calculation
			if i==0:
				self.adjArray.append([0])
			else:
				self.updateAdjacencyArray(i)


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
				Message.errorMessage()
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
					Message.errorMessage()
					continue

				#Check if it is the right dimension.
				if len(hSpace) != self.d+1:
					print('This list is the wrong length. Try again.')
				else:
					break
			
			#Add the halfspace to the list of halfspaces
			hSpaces.append(hSpace)



		return hSpaces


	#This method will check if the proposed region i overlaps with any previous region.
	def checkOverlap(self,candidatePoly,i):
		overlap = [False]
		for j in range(i):
			p = candidatePoly&self.regionsPoly[j]
			if p.dim()>=self.d:
				overlap.append(True)
				overlap.append(j)
		return overlap


	#This method will update the array of **relevant** adjacencies given this new region i.
	def updateAdjacencyArray(self,i):
		adjRow=[]
		for j in range(i):
			#Check if the region intersects with any other region.
			ijPoly=self.regionsPoly[i]&self.regionsPoly[j]
			if ijPoly.dim()>=0:
				#It does intersect with region j. It is possible that we will have to actually consider
				#adjacency as important information.
				adjacency = 1
				#Check all other intersections that region j has.
				for k in range(i):
					if self.adjArray[j][k]==0:
						#No need to check anything if j and k do not intersect.
						pass
					if self.adjArray[j][k]==1:
						#j and k do intersect. Does the candidate intersection subsume this intersection?
						#Does this intersection subsume the candidate intersection?
						kjPoly=self.regionsPoly[k]&self.regionsPoly[j]
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
							self.adjArray[j][k]=0
							self.adjArray[k][j]=0
						else:
							#Their symmetric difference is nonempty. No adjacencies are thrown away.
							pass
			#If they do not intersect, they are not adjacent in the first place.
			else:
				adjacency=0
			
			#Update the current row to indicate whether or not, for now, we are considering the ij adjacency
			#as important. Also update the j-th row to show this information in the standard symmetric fashion.
			adjRow.append(adjacency)
			self.adjArray[j].append(adjacency)

		#The final entry is the adjanceny of i with itself, which we consider to be 0 for simplification 
		adjRow.append(0)

		#Update the adjacency matrix by adding the new row.
		self.adjArray.append(adjRow)


	#This method returns takes the adjacency information about the regions and returns a properly labeled
	#graph.
	def makeGraph(self):
		#Make a graph from the adjacency matrix.
		adjmatrix=Matrix(self.adjArray)	
		self.adjGraph=Graph(adjmatrix)

		#Label the vertices with the appropriate region.
		keys=[]
		for i in range(self.n):
			keys.append(i)
		regionDictionary=dict(zip(keys,self.regionsPoly))
		self.adjGraph.set_vertices(regionDictionary)


	#Give an option to save this new space decomposition as a folder within the "Situations" folder.
	def saveSpaceDecomp(self):
		#Save the Space Decomp to the file structure created when setup.py is run
		while True:
			self.name = raw_input("Name your Space Decomp: ")
			currDir = os.getcwd()
			os.chdir(os.path.expanduser('~/Documents/Elvis/Situations'))
			try:
				os.makedirs(self.name)
				os.chdir(os.path.expanduser(self.name))
				saveDir = os.getcwd()
			except OSError as e:
				if e.errno != errno.EEXIST:
					Message.errorMessage()
				else:	
					print "ERROR... Already a saved space decomposition. \n"
				continue
			break

		sdFile = open("Space_Decomp_Info.txt","w+")
		sdFile.write(self.name + "\n")
		sdFile.write(str(self.d) + "\n")
		sdFile.write(str(self.n) + "\n")
		sdFile.write(str(self.adjArray) + "\n")
		sdFile.write(str(self.regionsText) + "\n")
		sdFile.close()
		os.chdir(os.path.expanduser(currDir))
		print  self.name + " saved to " + saveDir
