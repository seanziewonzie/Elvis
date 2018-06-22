import sys; sys.dont_write_bytecode = True
from sage.all import *
from Calculation import *
from Situation import *
import Message
#In Elvis, there are two kinds of objects which are stored on the memory drive: situations and calculations.
#This method will ask the user which kind of object they wish to deal with.
def firstChoice(self):
	while True:
		response = Message.getResponse('\nEnter 1 to get a calculation. \nEnter 2 to get a situation. \n')
		if response != '1' and response != '2':
			print 'Please enter 1 or 2.' 
			continue
		#Get a calculation, and handle it until the user asks to return to the beginning.
		if response == '1':
			calc=Calculation()
			calculation=calc.calculationLoadOrNew()
			calc.handleCalculation(calculation)
		#Get a situation, and either view or edit it until the user asks to return to the beginning.
		if response =='2':
			sit=Situation()
			situation=sit.situationLoadOrNew()
			sit.viewOrEditSituation(situation)


def welcomeMessage(self):
	print('\n      ------------------------------\n       Thank you for using Elvis. \n      Enter q at any time to quit.\n      ------------------------------\n')


def main(self):
	self.welcomeMessage()
	self.firstChoice()

if __name__ == "__main__":
	main()
