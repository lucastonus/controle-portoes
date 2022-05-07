import requests

from Response import Response

class PingPong:

	SERVER_ADDRESS = ''

	TOKEN = ''

	def request(self, endpoint: str) -> Response:
		return requests.post(self.SERVER_ADDRESS + '/' + endpoint, headers={'Authorization': 'Bearer ' + self.TOKEN})

	def ping(self) -> bool:
		response = self.request('ping')
		return response.status_code == 200

	def connect(self) -> bool:
		self.request('connect')

if __name__ == '__main__':
	pingPong = PingPong()

	success = pingPong.ping()

	if (success == False):
		pingPong.connect()