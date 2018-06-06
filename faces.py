class PlaneDecomp:
	#plane decompisiton function
	#Prompt user for number of faces.

	global n
	faces=[]
	adjgraph=[]

	def main():
		n=(int)(input('How many faces? '))
		#For each face:
		for i in range(0,n):

			#Get number of halfspaces which define the face.
			m=(int)(input('How many halfspaces cut out face '+str(i+1)+'? '))

			#Determine the halfspaces which define the face.
			hspaces=[]
			for j in range(0,m):
				hspacenums = raw_input('Give a triple indicating a half-space: ').split(" ")#will take in a string of numbers separated by a space
				hspace = [float(num) for num in hspacenums]
				hspaces.append(hspace)

		#Store array of halfspaces in face array.
		faces.append(hspaces)
		
	if __name__ == "__main__":
		main()

		