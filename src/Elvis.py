from sage.all import *
from Calculation import *
from Situation import *
class Elvis:
	
	def main():
		response = raw_input('\nEnter c to get a calculation. \nEnter s to get a situation. \n')
		while response !='c' and response !='s':
			print('This is not a valid input. Please type c/s: ')
			response =raw_input('\nEnter c to create or load a calculation. \nEnter s to view or edit a created situation, or create a new situation. \n')
		if response == 'c':
			calc=Calculation()
			calculation=calc.calculationLoadOrNew()
			calc.handleCalculation(calculation)
		if response =='s':
			response = raw_input('\nEnter c to create a situation. \nEnter v to view information about a saved situation. \nEnter e to edit a saved situation. \n')
			while response !='c' and response !='v' and response != 'e':
				print('This is not a valid input. Please type c/v/e: ')
				response =raw_input('\nEnter c to create a situation. \n Enter v to view information about a saved situation. \nEnter e to edit a saved situation. \n')
			sit = Situation()
			if response == 'c':
				sit.createSituation()
			if response =='e':
				sit.editSituation()
			if response == 'v':
				return 'We have not yet coded a way to view a created situation'
	
		
	if __name__ == "__main__":
		main()
