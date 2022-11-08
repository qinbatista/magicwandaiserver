import os,subprocess
class Install:
	@staticmethod
	def get_required_packages():
		""" 加载要求列表 """
		packages = list()
		pypath = os.path.dirname(os.path.realpath(__file__))
		requirements_file = os.path.join(pypath, "requirements.txt")
		with open(requirements_file,encoding="utf-8") as req:
			for package in req.readlines():
				package = package.strip()
				if package and (not package.startswith("#")):
					packages.append(package)
		return packages
	def pip_installer(self):
		packages = self.get_required_packages()
		for package in packages:
			subprocess.call("pip3 install " + package)
			print(package,"已安装\n")
if __name__ == "__main__":
	Install().pip_installer()