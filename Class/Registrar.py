from .User import *

class Registrar(User):

	def __init__(self,x):
		User.__init__(self,x)

	def createCase(self):
		pass

	def updateCase(self):
		pass

	def getCaseStatus(self):
		pass

	def getAvailableSlots(self):
		pass

	def getPendingCases(self):
		pass

	def createUser(self):
		pass

	def deleteUser(self):
		pass

	def addMoney(self):
		pass

	def getUpcomingCases(self):
		pass

	def getResolvedCases(self):
		pass