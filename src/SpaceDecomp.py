from sage.all import *
class SpaceDecomp:
	global response
	response =""
	global spaceDecomp
	spaceDecomp=[]
	def __init__(self):
		self.response = response
		self.spaceDecomp= spaceDecomp
	
		
	def SpaceDecompChoice(self):
		self.response =raw_input('Do you want to use a saved space decomposition? ')
		while self.response !='y' and self.response !='n':
			print('This is not a valid input. Please type y/n: ')
			self.response =raw_input('Do you want to use a saved space decomposition? ')
		if self.response == 'y':
			print('We have not coded save and write yet')
			#return self.chooseSpaceDecomp()
		if self.response =='n':
			print('You will now create a new space decomposition.')
			return self.createSpaceDecomp()
		
	
	
	def createSpaceDecomp(self):
		d=(int)(input('What is the dimension? '))
		n=(int)(input('How many regions? '))
		#the array of regions
		regions=[]
		#the simplified/optimized adjacency graph of the regions
		adjarray=[]		
		for i in range(n):
			while True:
				#Get number of halfspaces which define the face.
				m=(int)(input('How many halfspaces cut out region '+str(i+1)+'? '))
				#Determine the halfspaces which define the face.
				hspaces=[]
				for j in range(m):
					while True:
						if j==0:
							rawnums = raw_input('Give a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'st halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						elif j==1:
							rawnums = raw_input('Give a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'nd halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						elif j==2:
							rawnums = raw_input('Give a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'rd halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						else:
							rawnums = raw_input('Give a list of ' + str(d + 1) + ' numbers to indicate the ' +str(j+1) +'th halfspace, where a0 a1 ... an indicates the halfspace corresponsing to the inqeuality a0 + a1x1 + ... anxn <= 0 \n').split(" ") 
						#will take in a string of numbers separated by a space
						if len(rawnums) != d+1:
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
				adjarray.append([0])
			else:
				for j in range(i):
					#This will check the possible adjacency of the new region and another region
					ijPoly=Polyhedron(ieqs=regions[i]+regions[j])
					if p.dim()>=0:
						adjacency=1
						#Check against every other adjacency and see if this new adjacency is subsumed by it, or subsumes it
						for k in range(i):
							if adjarray[j][k]==0:
								adjacency=1
								#no need to check against an adjacency which doesn't exist
							if adjarray[j][k]==1:
								kjPoly=Polyhedron(ieqs=regions[k]+regions[j])
								if kjPoly&ijPoly==ijPoly:
									adjacency=adjacency*0
								if kjPoly&ijPoly==kjPoly:=[d,n,adjGraph]
									adjacency=adjacency*1
									adjarray[k][j]=0
									adjarray[j][k]=0
								if kjPoly!=ijPoly:
									if kjPoly&ijPoly==ijPoly:
										adjacency=0
										print('The intersection of ' + str(i) +' and ' + str(j) + ' is subsumed by the intersection of regions ' + str(k) + ' and ' + str(j))
										break
									if kjPoly&ijPoly==kjPoly:
										adjarray[k][j]=0
										adjarray[j][k]=0

					else:
						adjacency=0
						print('Regions ' + str(i) + ' and ' + str(j) + ' dont intersect')
					adjrow.append(adjacency)
					adjarray[j].append(adjacency)
				#The final entry is the adjanceny of i with itself, which we consider to be 0 for simplification 
				adjrow.append(0)
				adjarray.append(adjrow)
		keys=[]
		for i in range(n):
			keys.append(i)
		regionDictionary=dict(zip(keys,regions))
		adjmatrix=Matrix(adjarray)	
		adjGraph=Graph(adjmatrix)
		adjGraph.set_vertices(regionDictionary)
		self.spaceDecomp =[d,n,adjGraph]
		return self.spaceDecomp

	
