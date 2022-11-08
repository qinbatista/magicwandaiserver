import sys, os
import socket
import threading
from time import ctime

def DeployServer():
	os.chdir(os.getcwd())
	os.system("apt-get update")
	os.system("apt-get -y install apache2")
	os.system("cp -rf lukseun/ /var/www/")
	os.system("cp 000-default.conf /etc/apache2/sites-available/000-default.conf")
	os.system("/etc/init.d/apache2 restart")
def main():
	DeployServer()
if __name__ == '__main__':
    main()