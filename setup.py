import os
import subprocess
import platform

def main():
	Construct()
	print platform.system()

def Construct():
	os.mkdir("Calculations")
	os.mkdir("Situations")
	os.chdir("Situations")
	os.mkdir("SpaceDecompExampleFolder")

if __name__ == "__main__":
	main()
	
