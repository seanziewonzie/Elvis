import sys; sys.dont_write_bytecode = True
import random
#The generic error message for all generic errors we catch. We randomize the message so that 
#the text on screen does not seem unchanging/unresponsive.
def errorMessage():
	e = random.randint(1,3)
	if e % 2 == 0:
		print('\nSomething about that input was not right. Please try again. \n')
	if e % 2 == 1:
		print('\nThat was entered incorrectly. \n')


#Let's a user type in a response as an answer to an input question. Before returning the response,
#check if it is 'q' -- if it is, quit the program.
def getResponse(string):
	response = raw_input(string)
	if response == 'q':
		print 'quitting...'
		sys.exit(1)
	return response
