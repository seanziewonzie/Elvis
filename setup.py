import os
import subprocess
import platform

def main():
	Construct()
	print platform.system()

def Construct():
	os.mkdir("Calculations")
	os.mkdir("Situations")

if __name__ == "__main__":
	main()
	
