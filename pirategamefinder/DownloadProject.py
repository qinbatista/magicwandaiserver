import os
import time 
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def main():
	while(True):
		os.chdir(PythonLocation())
		os.system("git pull")
		time.sleep(5)
if __name__ == '__main__':
	main()