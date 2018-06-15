import sys; sys.dont_write_bytecode = True
from sage.all import *
from ErrorMessage import *
class StartAndEnd:
	def __init__(self,situation):
		self.situation = situation


	#This method bundles all the information about the start and end points into one array.
	def createStartAndEnd(self):
		start = self.pointInfo("start")
		end = self.pointInfo("end")
		return [start,end]


	#This method bundles all the information about any of the two points into one array.
	def pointInfo(self,string):
		#Gather all the parameters from the space decomposition to check the proposed points
		#against.
		spaceDecomp = self.situation[0]
		d = spaceDecomp[0]
		n = spaceDecomp[1]
		adjGraph = spaceDecomp[2]

		#This will prompt the user to input a (valid) point.
		while True:
			try:
				rawCoords=raw_input('\nWhat are the coordinates of the ' +string +'ing point? \n').split(" ")
				coords = [float(num) for num in rawCoords]
			except:
				if rawCoords == 'q':
					raise SystemExit
				err=ErrorMessage()
				err.errorMessage()
				continue
			#This point will have to prove that it is sensible and that it is contained in some region.
			contained = 0
			if len(coords)!=d:
				print('The '+ string +'ing point should be specified by ' + str(d) + ' coordinates. Try again. ')
				continue
			else:
				#Get the first region the point is contained in. 
				for i in  range(n):
					P = adjGraph.get_vertex(i)
					if P.contains(coords):
						contained = 1
						region = i 
						break
			#If the point was actually not contained in any region, this process will loop until the point is valid.
			if contained ==1:
				break
			else:
				print('This point is not contained in any region. Try again. ')

		#Both the coordinates and which region the point is in are bundled together in one array,
		#as they are both important information about the point.
		return [coords,region]