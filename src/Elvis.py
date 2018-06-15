import sys; sys.dont_write_bytecode = True
from sage.all import *
from Calculation import *
from Situation import *
class Elvis:
	#In Elvis, there are two kinds of objects which are stored on the memory drive: situations and calculations.
	#This method will ask the user which kind of object they wish to deal with.
	def firstChoice(self):
		response = raw_input('\nEnter 1 to get a calculation. \nEnter 2 to get a situation. \n')
		if response == 'q':
			exit()
		while response != '1' and response != '2':
			response =raw_input('Please enter 1 or 2. \nEnter 1 to get a calculation. \nEnter 2 to get a situation. \n')
		#Get a calculation, and handle it until the user asks to return to the beginning.
		if response == '1':
			calc=Calculation()
			calculation=calc.calculationLoadOrNew()
			while response == '1':
				response = calc.handleCalculation(calculation)
			self.firstChoice()
		#Get a situation, and either view or edit it until the user asks to return to the beginning.
		if response =='2':
			sit=Situation()
			situation=sit.situationLoadOrNew()
			while response != '3':
				response = sit.viewOrEditSituation(situation)
			self.firstChoice()

	def welcomeMessage(self):
		print('Thank you for using Elvis. \nEnter q at any time to quit.')


	def main(self):
		self.welcomeMessage()
		self.firstChoice()

if __name__ == "__main__":
	use = Elvis()
	use.main()