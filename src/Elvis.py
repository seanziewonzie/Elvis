import sys; sys.dont_write_bytecode = True
from sage.all import *
import CalculationsAndSituations as CAS
import Message
import os
import subprocess
import platform
#In Elvis, there are two kinds of objects which are stored on the memory drive: situations and calculations.
#This method will ask the user which kind of object they wish to deal with.
def firstChoice():
	#Keep looping the program from the beginning until the user quits somewhere.
	while True:
		response = Message.getResponse('\nEnter 1 to deal with a calculation. \nEnter 2 to deal with a situation. \n')
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



#Hi!
def welcomeMessage():
	print('\n      ----------------------------\n       Thank you for using Elvis. \n      Enter q at any time to quit.\n      ----------------------------\n')


#Check if the ElvisFiles folder has already been created. If not, create it. If so,
#continue with the program.
def needSetup():
	CURR_DIR = os.getcwd()
	try:
		os.chdir(os.path.expanduser("~/Documents/ElvisFiles"))
	except:
		Setup()
	os.chdir(CURR_DIR)


#Create ElvisFiles and populate it with the Calculations folder and the Situations folder.
def Setup():
	os.chdir(os.path.expanduser("~/Documents"))
	os.mkdir("ElvisFiles")
	os.chdir(os.path.expanduser("ElvisFiles/"))
	os.mkdir("Calculations")
	os.mkdir("Situations")


#Men want to be him. Women want to be *with* him. He's... main()!
def main():
	needSetup()
	welcomeMessage()
	firstChoice()

if __name__ == "__main__":
	main()
