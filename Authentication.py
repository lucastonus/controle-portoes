from DBConn import DBConn
from flask import request

class Authentication:
	ADMIN = 1
	idUser = 0

	def __init__(self, authAdmin: bool = True):
		self.__authAdmin = authAdmin

	def isAuthenticated(self, request: request) -> list:
		isAdmin = False
		isAuthenticated = False

		if ('Authorization' in request.headers):
			authorization = request.headers['Authorization'].split(' ')
			auth_key = authorization[1] if len(authorization) > 1 else authorization[0]

			db = DBConn()
			result = db.select('SELECT id FROM user WHERE auth_key = %s AND status = %s', [auth_key, 1])
			isAuthenticated = len(result)
			isAdmin = (isAuthenticated and result[0][0] == self.ADMIN)
			self.setIdUser(result[0][0] if isAuthenticated else 0)

		return isAdmin if self.__authAdmin else isAuthenticated

	def setIdUser(self, idUser):
		self.idUser = idUser

	def getIdUser(self):
		return self.idUser