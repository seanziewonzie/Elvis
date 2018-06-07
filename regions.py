#plane decompisiton function
#Prompt user for number of faces.
from sage.all import *

global n
regions=[]
adjgraph=[]

def main():
	d=(int)(input('What is the dimension? '))
	n=(int)(input('How many regions? '))
	#For each face:
	for i in range(0,n):
		while True:
			#Get number of halfspaces which define the face.
			m=(int)(input('How many halfspaces cut out region '+str(i+1)+'? '))
			#Determine the halfspaces which define the face.
			hspaces=[]
			for j in range(0,m):
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
						print('This list is the wrong length. Try again.')
					else:
						break
				hspace = [float(num) for num in rawnums]
				hspaces.append(hspace)
			overlap=0
			for j in range(0,i):
				intersection = hspaces + regions[j]
				p=Polyhedron(ieqs=intersection)
				if p.dim()>=d:
					print('This region overlaps with region ' + str(j+1) +'. Try again.')
					overlap=1
					break
			if overlap == 0:
				break
		regions.append(hspaces)
				
	#Store array of halfspaces in face array.
	
	print(regions)
	
if __name__ == "__main__":
	main()
