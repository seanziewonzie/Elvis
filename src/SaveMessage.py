class SaveMessage:
	def __init__(self,string):
		self.string = string

	def message(self):
		saveOption = raw_input('\nEnter s to save this ' + self.string +'. \nEnter anything else to move on without saving. \n')
		if saveOption == 'q':
			exit()
		if saveOption == 's':
			print('Saving is not a feature yet. ')
