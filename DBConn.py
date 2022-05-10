import sqlite3

class DBConn:

	def get_conn(self) -> object:
		return sqlite3.connect('controle_portoes.db')

	def insert(self, query: str, values: tuple) -> int:
		conn = self.get_conn()
		cursor = conn.cursor()
		cursor.execute(query, values)
		conn.commit()
		return conn.total_changes

	def select(self, query: str, values: tuple) -> list:
		conn = self.get_conn()
		cursor = conn.cursor()
		cursor.execute(query, values)
		return cursor.fetchall()