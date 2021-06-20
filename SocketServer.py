from DBConn import DBConn
from Response import Response
from ResponseMessage import ResponseMessage
import json
import socket
import threading

class SocketServer:

	socket = None

	client = None
	client_address = None

	GATE_OUTSIDE = 1
	GATE_INSIDE = 2
	GATE_BOTH = 3

	TIMEOUT_SECONDS = 30

	def init(self, host: str, port: int) -> tuple:
		if (self.socket == None):
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.settimeout(self.TIMEOUT_SECONDS)

			try:
				self.socket.bind((host, port))
				self.socket.listen()
				return Response(ResponseMessage.SERVER_STARTED_SUCCESSFULLY).create()
			except socket.error as msg:
				self.socket = None
				return Response(ResponseMessage.SERVER_ERROR_ON_START).create(msg)
		else:
			return Response(ResponseMessage.SERVER_ALREADY_STARTED).create()

	def accept_connection(self) -> tuple:
		if (self.socket != None):
			try:
				self.stop_client()
				client, address = self.socket.accept()
				threading._start_new_thread(self.new_client, (client, address))
				return Response(ResponseMessage.CLIENT_CONNECTED_SUCCESSFULLY).create()
			except socket.timeout:
				return Response(ResponseMessage.CLIENT_CONNECTION_TIMED_OUT).create(self.TIMEOUT_SECONDS)
		else:
			return Response(ResponseMessage.SERVER_NOT_STARTED).create()

	def stop(self) -> tuple:
		self.stop_client()

		if (self.socket != None):
			self.socket.close()
			self.socket = None
			return Response(ResponseMessage.SERVER_STOPPED_SUCCESSFULLY).create()
		else:
			return Response(ResponseMessage.SERVER_ALREADY_STOPPED).create()

	def new_client(self, client, address) -> None:
		self.client = client
		self.client_address = address

	def stop_client(self) -> None:
		if (self.client != None):
			self.client.close()
			self.client = None

	def send_message(self, message: str) -> tuple:
		try:
			self.client.sendall(bytearray([1, 125]) + bytes(message, 'utf-8'))
			return Response(ResponseMessage.CLIENT_MESSAGE_SENT).create()
		except BrokenPipeError:
			self.stop_client()
			return Response(ResponseMessage.CLIENT_CONNECTION_LOST).create()

	def status(self):
		return {}, 200

	def open_gates(self, payload: dict, id_user: int) -> tuple:
		if (self.client != None):
			if (payload != None and 'gate' in payload):
				payload_gate = int(payload['gate'])

				if (payload_gate in [self.GATE_OUTSIDE, self.GATE_INSIDE, self.GATE_BOTH]):
					gate = payload_gate

					result = self.send_message(json.dumps(payload))
					if (result[1] == ResponseMessage.HTTP_CODE['OK']):
						DBConn().insert('INSERT INTO log (id_user, gate) VALUES (%s, %s)', [id_user, gate])

					return result
				else:
					return Response(ResponseMessage.INVALID_GATE).create()
			else:
				return Response(ResponseMessage.GATE_NOT_INFORMED).create()
		else:
			return Response(ResponseMessage.CLIENT_NOT_CONNECTED).create()
