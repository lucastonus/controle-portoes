import json

class Response:

	response = None

	CONTENT_TYPE = {
		'ContentType': 'application/json'
	}

	def __init__(self, response: dict):
		self.response = response

	def message(self, args: tuple = ()) -> tuple:
		return json.dumps({'message': self.response['message'] % args}, ensure_ascii=False).encode('utf8'), self.response['http_code'], self.CONTENT_TYPE

	def data(self, args: object = {}) -> tuple():
		return json.dumps(args, ensure_ascii=False).encode('utf8'), self.response['http_code'], self.CONTENT_TYPE