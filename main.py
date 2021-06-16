from flask import Flask, request
from SocketServer import SocketServer
from Authentication import Authentication
from typing import Callable
import json
import socket

app = Flask('GatesAPI')

socketServer = SocketServer()

def auth(callback: Callable, request: request, admin: bool = True):
	authentication = Authentication(admin)
	if (authentication.isAuthenticated(request)):
		return callback(authentication.getIdUser()) if admin == False else callback()
	else:
		return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}

@app.route('/start', methods=['POST'])
def start():
	return auth(lambda: socketServer.init('', 7777), request)

@app.route('/stop', methods=['POST'])
def stop():
	return auth(lambda: socketServer.stop(), request)

@app.route('/connect', methods=['POST'])
def connect():
	try:
		return auth(lambda: socketServer.acceptConnection(), request)
	except socket.timeout:
		return json.dumps({'success': False}), 408, {'ContentType': 'application/json'}

@app.route('/gates', methods=['POST'])
def gates():
	return auth(lambda idUser: socketServer.openGates(request.get_json(), idUser), request, False)