from sage.all import *
from Calculation import *
from Situation import *
class Elvis:
	
	def main():
		response = raw_input('Enter c to create or load a calculation. Enter s to view or edit a created situation. ')
		while response !='c' and response !='s':
			print('This is not a valid input. Please type c/s: ')
			response =raw_input('Enter c to create or load a calculation. Enter s to view or edit a created situation, or create a new situation. ')
		if response == 'c':
			self.Calculation()
		if response =='s':
			self.Situation()
		
		
	def Calculation():
		calc=Calculation()
		calculation=calc.calculationLoadOrNew()
		calc.handleCalculation(calculation)
		
	def  Situation():
		response = raw_input('Enter c to create a situation. Enter v to view information about a saved situation. Enter e to edit a saved situation. ')
		while response !='c' and response !='v' and response != 'e':
			print('This is not a valid input. Please type c/v/e: ')
			response =raw_input('Enter c to create a situation. Enter v to view information about a saved situation. Enter e to edit a saved situation. ')
		sit = Situation()
		if response == 'c':
			sit.createSituation
		if response =='e':
			sit.editSituation()
		if response == 'v'
		
		return 'We have not yet coded a way to view or edit a created situation'
		
	if __name__ == "__main__":
		main()
