import sys; sys.dont_write_bytecode = True
import random
class ErrorMessage():
	#The error message for all caught exceptions.
	def errorMessage(self):
		e = random.randint(1,3)
		if e % 2 == 0:
			print('\nSomething about that input was not right. Please try again. \n')
		if e % 2 == 1:
			print('\nThat was entered incorrectly. \n')