from flask import Flask, request
from SocketServer import SocketServer
from Authentication import Authentication
from Response import Response
from ResponseType import ResponseType
from typing import Callable

app = Flask('GatesAPI')

socket_server = SocketServer()

def auth(callback: Callable, request: request, admin: bool = True, id_user: bool = False) -> tuple:
	authentication = Authentication(admin)
	if (authentication.is_authenticated(request)):
		return callback(authentication.get_id_user()) if id_user else callback()
	else:
		return Response(ResponseType.INVALID_CREDENTIALS).message()

@app.route('/start', methods=['POST'])
def start() -> tuple:
	return auth(lambda: socket_server.init('', SocketServer.SOCKET_PORT), request)

@app.route('/stop', methods=['POST'])
def stop() -> tuple:
	return auth(lambda: socket_server.stop(), request)

@app.route('/connect', methods=['POST'])
def connect() -> tuple:
	return auth(lambda: socket_server.accept_connection(), request)

@app.route('/gates', methods=['POST'])
def gates() -> tuple:
	return auth(lambda idUser: socket_server.open_gates(request.get_json(), idUser), request, False, True)

@app.route('/status', methods=['GET'])
def status() -> tuple:
	return auth(lambda: socket_server.status(), request, False)