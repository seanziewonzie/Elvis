import sys; sys.dont_write_bytecode = True
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
		subprocess.call("start","cmd")
		os.chdir(os.path.expanduser("%userprofile%"))
		os.chdir(os.path.expanduser("%userprofile%\Documents\Elvis"))
		subprocess.call(["mkdir","Calculations"])
		subprocess.call(["mkdir","Situations"])
		os.chdir(os.path.expanduser("%userprofile%\Documents\Elvis\Situations"))
		subprocess.call(["mkdir","SpaceDecompExampleFolder"])

if __name__ == "__main__":
	main()	