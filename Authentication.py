from DBConn import DBConn
from flask import request

class Authentication:

	ADMIN = 1
	id_user = 0

	def __init__(self, auth_admin: bool = True):
		self.__auth_admin = auth_admin

	def is_authenticated(self, request: request) -> list:
		is_admin = False
		is_authenticated = False

		if ('Authorization' in request.headers):
			authorization = request.headers['Authorization'].split(' ')
			auth_key = authorization[1] if len(authorization) > 1 else authorization[0]

			result = DBConn().select('SELECT id FROM user WHERE auth_key = ? AND status = ?', [auth_key, 1])
			is_authenticated = len(result)
			is_admin = (is_authenticated and result[0][0] == self.ADMIN)
			self.set_id_user(result[0][0] if is_authenticated else 0)

		return is_admin if self.__auth_admin else is_authenticated

	def set_id_user(self, id_user) -> None:
		self.id_user = id_user

	def get_id_user(self) -> int:
		return self.id_user