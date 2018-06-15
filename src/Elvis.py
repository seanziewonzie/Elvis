from sage.all import *
from Calculation import *
from Situation import *
class Elvis:
	

	def main():
		self.firstChoice()


	#In Elvis, there are two kinds of objects which are stored on the memory drive: situations and calculations.
	#This method will ask the user which kind of object they wish to deal with.
	def firstChoice(self):
		response = raw_input('\nEnter 1 to get a calculation. \nEnter 2 to get a situation. \n')
		while response != 1 and response != 2:
			response =raw_input('Please enter 1 or 2. \nEnter 1 to get a calculation. \nEnter 2 to get a situation. \n')
			#Get a calculation.

		#Get a calculation, and handle it until the user asks to return to the beginning.
		if response == '1':
			calc=Calculation()
			calculation=calc.calculationLoadOrNew()
			while response == '1':
				response = calc.handleCalculation(calculation)
			self.main()

		#Get a situation, and either view or edit it until the user asks to return to the beginning.
		if response =='2':
			sit=Situation()
			situation=sit.situationLoadOrNew()
			while response != '3':
				response = sit.viewOrEditSituation(situation)
			self.main()
			
	#The error message for all caught exceptions.		
	def errorMessage():
		print('\nSomething about that was not right. Try again. \n')
		
	if __name__ == "__main__":
		main()
