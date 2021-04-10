class User:
	# _name = ""
	# _username = ""
	# _password = ""
	# _type = ""
	# _isloggedin = False

	def __init__(self,x):
		self._username = x[1]
		self._type = x[0]
		self._password = x[2]
		self._isloggedin = True
		self._name = x[3]

	def login(self):
		_isloggedin = True

	def logout(self):
		_isloggedin = False

	def getType(self):
		return self._type

	def getName(self):
		return self._name

	def getUsername(self):
		return self._username

	def isloggedin(self):
		return self._isloggedin