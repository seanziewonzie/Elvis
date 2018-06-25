import sys; sys.dont_write_bytecode = True
import random
#The error message for all caught exceptions.
def errorMessage():
	e = random.randint(1,3)
	if e % 2 == 0:
		print('\nSomething about that input was not right. Please try again. \n')
	if e % 2 == 1:
		print('\nThat was entered incorrectly. \n')


def getResponse(string):
	response = raw_input(string)
	if response == 'q':
		print 'quitting...'
		sys.exit(1)
	return response
