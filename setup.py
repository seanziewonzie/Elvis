import os
import subprocess
import platform

def main():
	Construct()
	print platform.system()

def Construct():

	yourOS = platform.system()
	if yourOS == "Linux":
		subprocess.call(["mkdir","Calculations"])
		subprocess.call(["mkdir","Situations"])
		os.chdir(os.path.expanduser("~/Documents/Elvis/Situations"))
		subprocess.call(["mkdir","SpaceDecompExampleFolder"])

	if yourOS == "Windows":
		os.mkdir("Calculations")
		os.mkdir("Situations")
		os.chdir("Situations")
		os.mkdir("SpaceDecompExampleFolder")

if __name__ == "__main__":
	main()
	
