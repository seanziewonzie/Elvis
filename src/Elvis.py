import sys; sys.dont_write_bytecode = True
from sage.all import *
import CalculationsAndSituations as CAS
import Message
#In Elvis, there are two kinds of objects which are stored on the memory drive: situations and calculations.
#This method will ask the user which kind of object they wish to deal with.
def firstChoice():
	#Keep looping the program from the beginning until the user quits somewhere.
	while True:
		response = Message.getResponse('\nEnter 1 to get a calculation. \nEnter 2 to get a situation. \n')
		if response != '1' and response != '2':
			print 'Please enter 1 or 2.' 
			continue
		#Get a calculation, and handle it until the user asks to return to the beginning.
		if response == '1':
			calc=CAS.Calculation()
			calc.calculationLoadOrNew()
			calc.handleCalculation()
		#Get a situation, and either view or edit it until the user asks to return to the beginning.
		if response =='2':
			sit=CAS.Situation()
			sit.situationLoadOrNew()
			sit.viewOrEditSituation()


def welcomeMessage():
	print('\n      ------------------------------\n       Thank you for using Elvis. \n      Enter q at any time to quit.\n      ------------------------------\n')


def main():
	welcomeMessage()
	firstChoice()

if __name__ == "__main__":
	main()
