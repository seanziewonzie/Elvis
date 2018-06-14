from sage.all import *
class StartAndEnd:
	def __init__(self,situation):
		self.situation = situation

	def createStartAndEnd(self):
		start = self.pointInfo("start")
		end = self.pointInfo("end")
		return [start,end]

	def pointInfo(self,string):
		spaceDecomp = self.situation[0]
		d = spaceDecomp[0]
		n = spaceDecomp[1]
		adjGraph = spaceDecomp[2]

		while True:
			contained = 0
			rawCoords=raw_input('\nWhat are the coordinates of the ' +string +'ing point? \n').split(" ")
			if len(rawCoords)!=d:
				print('The '+ string +'ing point should be specified by ' + str(d) + 'coordinates. Try again. ')
			else:
				coords = [float(num) for num in rawCoords]
				for i in  range(n):
					P = adjGraph.get_vertex(i)
					if P.contains(coords):
						contained = 1
						region = i 
						break
			if contained ==1:
				break
			else:
				print('This point is not contained in any region. Try again. ')

		return [coords,region]
