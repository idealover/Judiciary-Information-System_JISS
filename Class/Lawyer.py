from .User import *

class Lawyer(User):

	def __init__(self,x):
		User.__init__(self,[x[0],x[1],x[2],x[3]])
		self._money = x[4]

	def getCaseDetails(self):
		pass

	def addMoney(self,n):
		self._money+=n

	def getMoney(self):
		return self._money

	def subtractMoney(self):
		self._money -= 5