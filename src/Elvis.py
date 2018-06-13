from sage.all import *
from Calculations import *
class Elvis:
	
	def main():
		calc=Calculations()
		calculation=calc.calculationLoadOrNew()
		calc.handleCalculation(calculation)
		
		
	if __name__ == "__main__":
		main()
