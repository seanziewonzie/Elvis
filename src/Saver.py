import os
import subprocess
import platform

def main():
	Construct()
	print platform.system()

def Construct():
	yourOS = platform.system()
	if yourOS == "Linux":
		os.chdir(os.path.expanduser("~/Documents/"))
		subprocess.call(["mkdir","Elvis"])
		os.chdir(os.path.expanduser("~/Documents/Elvis"))
		subprocess.call(["mkdir","Calculations"])
		subprocess.call(["mkdir","Situations"])
		os.chdir(os.path.expanduser("~/Documents/Elvis/Situations"))
		subprocess.call(["mkdir","SpaceDecomp"])
	if yourOS == "Windows":
		subprocess.call("start","cmd")
		os.chdir(os.path.expanduser("%userprofile%"))
		subprocess.call(["mkdir","Elvis"])
		os.chdir(os.path.expanduser("%userprofile%\Documents\Elvis"))
		subprocess.call(["mkdir","Calculations"])
		subprocess.call(["mkdir","Situations"])
		os.chdir(os.path.expanduser("%userprofile%\Documents\Elvis\Situations"))
		subprocess.call(["mkdir","SpaceDecomp"])

def Save():


if __name__ == "__main__":
	main()
	
