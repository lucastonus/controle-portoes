from flask import Flask, request
from flask.views import MethodView

app = Flask('GatesAPI')

def init(socketServer):
	routes(socketServer)
	app.run(port=81)

def routes(socketServer):
	@app.route('/gates', methods=['POST'])
	def gates():
		payload = request.get_json()
		return socketServer.sendMessage(payload)