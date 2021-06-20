import mysql.connector

class DBConn:

	def get_conn(self) -> object :
		return mysql.connector.connect(
			host='127.0.0.1',
			user='root',
			password='password',
			database='controle_portoes'
		)

	def insert(self, query: str, values: tuple) -> int:
		conn = self.get_conn()
		cursor = conn.cursor()
		cursor.execute(query, values)
		conn.commit()
		return cursor.rowcount

	def select(self, query: str, values: tuple) -> list:
		conn = self.get_conn()
		cursor = conn.cursor()
		cursor.execute(query, values)
		return cursor.fetchall()
