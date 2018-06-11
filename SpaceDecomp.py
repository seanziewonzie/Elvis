#plane decompisiton function
#Prompt user for number of faces.

#subprocess allows us to run Linux commands from the python script
import errno
import subprocess
import os
from sage.all import *

class SpaceDecomp:
	#the array of regions
	regions=[]

	#the simplified/optimized adjacency graph of the regions
	adjgraph=[]

	#variable to distinguish test session vs real use
	global t
	t= ""

	global m
	m=0
	global n
	n = 0
	global d
	d = 0
	
	def __init__(self,d,n):
		self.n = n
		self.d = d
	def getGraph(self):
		
		t=raw_input("Save data? y/n: ")
		t=str(t)

		
	
		for i in range(self.n):
			while True:
				#Get number of halfspaces which define the face.
				m=(int)(input('How many halfspaces cut out region '+str(i+1)+'? '))
				#Determine the halfspaces which define the face.
				hspaces=[]
				for j in range(m):
					while True:
						if j==0:
							rawnums = raw_input('Give a list of ' + str(self.d + 1) + ' numbers to indicate the ' +str(j+1) +'st halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						elif j==1:
							rawnums = raw_input('Give a list of ' + str(self.d + 1) + ' numbers to indicate the ' +str(j+1) +'nd halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						elif j==2:
							rawnums = raw_input('Give a list of ' + str(self.d + 1) + ' numbers to indicate the ' +str(j+1) +'rd halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
					else:
						rawnums = raw_input('Give a list of ' + str(self.d + 1) + ' numbers to indicate the ' +str(j+1) +'th halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						#will take in a string of numbers separated by a space
					if len(rawnums) != self.d+1:
						#This checks if the halfspace is the right dimension
						print('This list is the wrong length. Try again.')
					else:
						break
					hspace = [float(num) for num in rawnums]
					hspaces.append(hspace)
					#The user will keep inputting the region until it does not intersect with previous regions
				overlap=0
				for j in range(0,i):
					p=Polyhedron(ieqs=hspaces + regions[j])
					if p.dim()>=d:
						print('This region overlaps with region ' + str(j+1) +'. Try again.')
						overlap=1
						break
				if overlap == 0:
					break
			regions.append(hspaces)
			adjrow=[]
			#This will constantly update the graph so that two regions are adjacent if and only if their intersection is not subsumed by another intersection
			if i==0:
				adjgraph.append([0])
			else:
				for j in range(i):
					#This will check the possible adjacency of the new region and another region
					ijPoly=Polyhedron(ieqs=regions[i]+regions[j])
					if p.dim()>=0:
						adjacency=1
						#I will check against every other adjacency and see if this new adjacency is subsumed by it, or subsumes it
						for k in range(i):
							if adjgraph[j][k]==0:
								adjacency=1
								#no need to check against an adjacency which doesn't exist
							if adjgraph[j][k]==1:
								kjPoly=Polyhedron(ieqs=regions[k]+regions[j])
								if kjPoly&ijPoly==ijPoly:
									adjacency=adjacency*0
								if kjPoly&ijPoly==kjPoly:
									adjacency=adjacency*1
									adjgraph[k][j]=0
									adjgraph[j][k]=0
					else:
						adjacency=0
					adjrow.append(adjacency)
					adjgraph[j].append(adjacency)
				#The final entry is the adjanceny of i with itself, which we consider to be 0 for simplification 
				adjrow.append(0)
				adjgraph.append(adjrow)
			
	
	
		for i in range(0,self.n):
			print('This is region ' + str(i+1))
			print(regions[i])
		
		for i in range(0,n):
			guprint(adjgraph[i])
			print('This is the adjacency graph')
	#method to save data, will either add similar method to each class or make standalone class to import		
	def save(self):
		if t == "y":
			#change working dir to /home/Documents
			os.chdir(os.path.expanduser("~/Documents"))
			try:
				#try and change working dir to /home/Documents/ElvisData
				os.chdir(os.path.expanduser("~/Documents/ElvisData"))
			except OSError as error:
				#if /home/Documents/ElvisData doesn't exits, create the dir in /home/Documents/
				if error.errno == errno.ENOENT:
					subprocess.call(["mkdir","ElvisData"]) 
				#change working dir to /home/Documents/ElvisData          
				os.chdir(os.path.expanduser("~/Documents/ElvisData"))
			finally:
				#create a file in /home/Documents/ElvisData
				subprocess.call(["touch",str(self.d)+"-dimens_"+str(self.n)+"-regions"+".txt"])


	if __name__ == "__main__":
		getGraph()
		save()
