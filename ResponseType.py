class ResponseType:

	HTTP_CODE = {
		'OK': 200,
		'BAD_REQUEST': 400,
		'UNAUTHORIZED': 401,
		'REQUEST_TIMEOUT': 408,
		'SERVICE_UNAVAILABLE': 503
	}

	CLIENT_CONNECTED_SUCCESSFULLY = {
		'http_code': HTTP_CODE['OK'],
		'message': 'O cliente foi conectado com sucesso'
	}

	CLIENT_MESSAGE_SENT = {
		'http_code': HTTP_CODE['OK'],
		'message': 'A mensagem foi enviada com sucesso'
	}

	CLIENT_PING = {
		'http_code': HTTP_CODE['OK'],
		'message': 'Ping enviado com sucesso'
	}

	SERVER_STARTED_SUCCESSFULLY = {
		'http_code': HTTP_CODE['OK'],
		'message': 'O servidor foi inicializado com sucesso'
	}

	SERVER_ALREADY_STARTED = {
		'http_code': HTTP_CODE['OK'],
		'message': 'O servidor já foi inicializado'
	}

	SERVER_STOPPED_SUCCESSFULLY = {
		'http_code': HTTP_CODE['OK'],
		'message': 'O servidor foi encerrado com sucesso'
	}

	SERVER_ALREADY_STOPPED = {
		'http_code': HTTP_CODE['OK'],
		'message': 'O servidor já está encerrado'
	}

	SERVER_STATUS = {
		'http_code': HTTP_CODE['OK']
	}

	GATE_NOT_INFORMED = {
		'http_code': HTTP_CODE['BAD_REQUEST'],
		'message': 'O portão não foi informado'
	}

	INVALID_GATE = {
		'http_code': HTTP_CODE['BAD_REQUEST'],
		'message': 'O portão informado é inválido'
	}

	INVALID_CREDENTIALS = {
		'http_code': HTTP_CODE['UNAUTHORIZED'],
		'message': 'Credenciais inválidas'
	}

	CLIENT_CONNECTION_TIMED_OUT = {
		'http_code': HTTP_CODE['REQUEST_TIMEOUT'],
		'message': 'Tempo de conexão excedido: %s segundos'
	}

	CLIENT_NOT_CONNECTED = {
		'http_code': HTTP_CODE['SERVICE_UNAVAILABLE'],
		'message': 'A conexão com o cliente não foi estabelecida'
	}

	CLIENT_CONNECTION_LOST = {
		'http_code': HTTP_CODE['SERVICE_UNAVAILABLE'],
		'message': 'A conexão com o cliente foi encerrada'
	}

	SERVER_ERROR_ON_START = {
		'http_code': HTTP_CODE['SERVICE_UNAVAILABLE'],
		'message': 'Erro ao inicializar o servidor: %s'
	}

	SERVER_NOT_STARTED = {
		'http_code': HTTP_CODE['SERVICE_UNAVAILABLE'],
		'message': 'O servidor não foi inicializado'
	}

	LOGS_DATA = {
		'http_code': HTTP_CODE['OK']
	}