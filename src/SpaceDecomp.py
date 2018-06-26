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


	#The user has decided to make a new space decomposition. They will now be asked if they want to make one from scratch or use a previous situation.
	def spaceDecompLoadOrNew(self):
		response = Message.getResponse('\nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
		while response!= '1' and response != '2':
			response = Message.getResponse('Please enter 1 or 2. \nPress 1 to load a space decomposition. \nPress 2 to create a new space decomposition. \n')
		if response == '1':
			self.chooseSpaceDecomp()
		if response =='2':
			print('\nYou will now create a new space decomposition.')
			self.createSpaceDecomp()


	#We let the user load a space decomposition from the Situations folder (and to help them, they can see which space decompositions are in the Situations folder).
	def chooseSpaceDecomp(self):
		#Show the user which saved space decompositions exist.
		os.chdir(os.path.expanduser("~/Documents/ElvisFiles/Situations"))
		print "\nYour saved space decompositions:"
		subprocess.call("ls")

		#The user will keep inputting space decompositions to load until they choose one which actually exists.
		while(True):
			chosenDecomp = Message.getResponse("\nSelect a space decomposition (case sensitive): ")
			try:
				os.chdir(os.path.expanduser(chosenDecomp))
				break
			except:
				if OSError.errno == errno.ENOENT:
					print "---That space decomposition does not exist, retry---"
				else:
					Message.errorMessage()

		#Populate all the variables with information from the text file.
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
		self.saveSpaceDecomp()


	#This method prompts the user for the dimension of space being simulated
	#and the number of polyhedral regions the space has been decomposed into.
	def getDimensionsAndRegions(self):
		#The user will keep inputting a dimension until it is actually an integer greater than 1.
		while True:
			raw=Message.getResponse('What is the dimension? ')
			try:	
				self.d=int(raw)
			except:
				Message.errorMessage()
				continue
			if self.d < 1:
				print 'There must be at least one spatial dimension. Try again.'
				continue
			break


		#The user will keep inputting a dimension until it is actually an integer greater than 1.
		while True:
			try:
				raw=Message.getResponse('How many regions? ')
				self.n = (int)(raw)
			except:
				Message.errorMessage()
				continue
			if self.n < 1:
				print 'There must be at least one region. Try again.'
				continue
			break


	#This method creates the polyhedral regions and updates a matrix which logs the **relevant** adjacencies.
	def createRegionsAndAdjacency(self):
		for i in range(self.n):
			#Construct a region. Before adding it to regions, check that it is defined by halfspaces of the correct dimension,
			#and that it it does not overlap with previous regions.
			while True:
				#Get a candidate for a text description of this polyhedron.
				candidateHSpaces = self.createCandidate(i)
				
				#Make a polyhedron out of these halfspaces.
				candidatePoly = Polyhedron(ieqs = candidateHSpaces)
				
				#No need to check for overlap if there are no previous regions. Move on to accept this candidate region into the
				#array of stored regions.
				if i == 0:
					break
				
				#Check for overlap.
				overlap= self.checkOverlap(candidatePoly,i)

				#If it overlaps, print which region it overlaps with.
				if overlap[0] == True:
					print ('This region overlaps with region ' + str(overlap[1]+1) +'. Try again.')
				
				#If it does not overlap with anything, move on to accept this candidate region into the array of stored regions.
				else:
					break
			
			#Accept this candidate region (in its text form and in its polyhedral object form) into the array of stored regions.
			self.regionsText.append(candidateHSpaces)
			self.regionsPoly.append(candidatePoly)


			#If this is the first region, the adjacency array is empty. For simplifications sake (and to abide by a graph theory
			#standard), we consider a region to not be adjacent to itself.
			if i==0:
				self.adjArray.append([0])

			#This will constantly update the adjacency matrix so that two regions are considered adjacent if and only if 
			#their intersection is not subsumed by another intersection.
			#If an intersection is subsumed by another intersection, it will be considered as a subcase later when the program
			#considers paths from intersection to intersection. So it may be thrown away to optimize the number of paths
			#handled in the calculation
			else:
				self.updateAdjacencyArray(i)


	#This method will get the halspaces that define a region, but it will check that the halfspaces are sensible.
	def createCandidate(self,i):
		#Ask the user how many halfspaces cut out this region. Keep asking until this is a positive integer.
		while True:
			raw=Message.getResponse('\nHow many halfspaces cut out region '+str(i+1)+'? ')
			try:
				m = (int)(raw)
			except:
				Message.errorMessage()
				continue
			if m < 0:
				print 'There cannot be a negative number of halfspaces'
				continue
			if m == 0:
				print 'There must be at least one halfspace which cuts out this region.\nIf you wish for you region to be all of space, split space into two regions and remember to always assign to each region the same velocity set.'
				continue			
			break

		#Get the list of halfspaces that will together cut out the proposed region i.	
		hSpaces=[]
		for j in range(m):
			#Keep asking for a list of numbers to describe the j-th halfspace until it is a sensible list of the correct length.
			while True:
				rawNums = Message.getResponse('\nGive a list of ' + str(self.d + 1) + ' numbers to indicate the ' +ordinator.ordinal(j+1)+ ' halfspace, \nwhere a0 a1 ... an indicates the halfspace corresponding to the inequality \na0 + a1*x1 + ... an*xn <= 0 \n')
				#Try and turn the response into a list of numbers.
				try:
					splitNums = rawNums.split(" ")
					hSpace = [float(num) for num in splitNums]
				except:
					Message.errorMessage()
					continue

				#Check if it is the right dimension.
				if len(hSpace) != self.d+1:
					print('This list is the wrong length. Try again.')
				else:
					break
			
			#Add the halfspace to the list of halfspaces.
			hSpaces.append(hSpace)
		return hSpaces


	#This method will check if the proposed region i overlaps with any previous region.
	def checkOverlap(self,candidatePoly,i):
		overlap = []
		for j in range(len(self.regionsPoly)):
			p = candidatePoly&self.regionsPoly[j]
			if p.dim()>=self.d:
				overlap.append(True)
				overlap.append(j)
			else:
				overlap.append(False)
		return overlap


	#This method will update the array of **relevant** adjacencies given this new region i.
	def updateAdjacencyArray(self,i):
		adjRow=[]
		for j in range(i):
			ijPoly=self.regionsPoly[i]&self.regionsPoly[j]

			#Check if the region i intersects with the region j.
			if ijPoly.dim()>=0:
				#It does intersect with region j. It is possible that we will have to actually consider
				#adjacency as important information.
				adjacency = 1

				#Generate all other intersections involving j. Check if this i-j intersection subsumes or is subsumed by
				#any of these intersections.
				for k in range(i):
					#No need to check against the j-k intersection if j and k do not intersect.
					if self.adjArray[j][k]==0:
						pass
					
					#j and k do intersect. Does the i-j intersection subsume this j-kintersection?
					#Does this j-k intersection subsume the i-j intersection?					
					if self.adjArray[j][k]==1:
						#Create the polytope corresponding to this intersection.
						kjPoly=self.regionsPoly[k]&self.regionsPoly[j]

						#If A subsumes B, then necessarily A intersection B is equal to B. However, if A and B were equal all along, this is not really
						#"subsuming", so we should check that first.
						
						#Neither subsumes the other. Both adjacencies may still be necessary to consider, so move along to the next k without changing
						#aything.
						if kjPoly == ijPoly:
							pass
						
						#The candidate intersection is subsumed. The adjacency between i and j will never be considered. Break everythin and move on to 
						#comparing i against a different j.
						elif kjPoly & ijPoly == ijPoly:
							adjacency = 0
							break
						
						#The i-j intersection subsumes the j-k intersection. Stop considering the j-k intersection.
						elif kjPoly & ijPoly == kjPoly:
							self.adjArray[j][k]=0
							self.adjArray[k][j]=0
			
			#If they do not intersect, they are not adjacent in the first place.
			else:
				adjacency=0
			
			#Update the current row to indicate whether or not, for now, we are considering the ij adjacency
			#as important. Also update the j-th row to show this information in the standard symmetric fashion.
			adjRow.append(adjacency)
			self.adjArray[j].append(adjacency)

		#The final entry is the adjanceny of i with itself, which we consider to be 0 for simplification/standardization reasons.
		adjRow.append(0)

		#Update the adjacency matrix by adding the new row.
		self.adjArray.append(adjRow)


	#This method returns takes the adjacency information about the regions and returns a properly labeled 
	#adjacency graph for the polyhedral regions of the space decomposition.
	def makeGraph(self):
		#Make a graph from the adjacency matrix.
		adjmatrix=Matrix(self.adjArray)	
		self.adjGraph=Graph(adjmatrix)

		#Label the vertices with the appropriate polyhedral region.
		keys=[]
		for i in range(self.n):
			keys.append(i)
		regionDictionary=dict(zip(keys,self.regionsPoly))
		self.adjGraph.set_vertices(regionDictionary)


	#Give an option to save this new space decomposition as a folder within the "Situations" folder.
	def saveSpaceDecomp(self):
		#Save the Space Decomp to the file structure created when setup.py is run
		save = Message.getResponse("Save this space decomposition(y/n): ")
		while save != "y" and save != "n":
			save = Message.getResponse("Error, type either y or n, retry: ")
		
		#They decided to save.
		if save == "y":
			#Mark the current directory, so we can return back to it after all of this writing.
			currDir = os.getcwd()
			
			#They will keep giving a name to the space decomposition until it both makes sense and is not already the name
			#of another saved space decomposition.
			while True:
				self.name = raw_input("Name your space decomposition. Do not use 'q' ")
				os.chdir(os.path.expanduser('~/Documents/ElvisFiles/Situations'))
				try:
					os.makedirs(self.name)
					os.chdir(os.path.expanduser(self.name))
					saveDir = os.getcwd()
				except:
					if OSError.errno != errno.EEXIST:
						Message.errorMessage()
					else:	
						print "ERROR... Already a saved space decomposition. \n"
					continue
				break

			#Make a folder to store all the velocity files this user will associate to this space decomposition in the future.
			os.makedirs('Velocities')

			#Write all of the relevant information to a text file.
			sdFile = open("Space_Decomp_Info.txt","w+")
			sdFile.write(self.name + "\n")
			sdFile.write(str(self.d) + "\n")
			sdFile.write(str(self.n) + "\n")
			sdFile.write(str(self.adjArray) + "\n")
			sdFile.write(str(self.regionsText) + "\n")
			sdFile.close()
			
			#Go back to the directory the user was in before this writing process.
			os.chdir(os.path.expanduser(currDir))
			
			#A confirmation message for the user.
			print  self.name + " saved to " + saveDir
