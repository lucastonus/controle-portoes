function init() {
	var deferredObjCreateHTML = createHTML();
	var deferredObjUpdateStyle = updateStyle();

	$.when(deferredObjCreateHTML, deferredObjUpdateStyle).done(function() {
		bindEvents();
		$('#div_remote_control').show();
		checkLogin();
	});
}

function bindEvents() {
	$(window).on('resize', function() {
		updateStyle();
	});

	$(document).on('click', '.btn, .btn-gates', function() {
		eventScreen('question', {'gate': $(this).attr('data-gate')});
	});

	$('#btn_yes').on('click', function() {
		openGate($(this).attr('data-gate'));
	});

	$('#btn_no').on('click', function() {
		if ($.cookie('SSID') != undefined) {
			eventScreen('logged');
		} else {
			eventScreen('login');
		}
	});

	$(document).on('click', '#btn_ok', function() {
		if ($(this).attr('data-action') == 'ok') {
			eventScreen('login');
		} else {
			$.ajax({
				'type': 'GET',
				'url': 'http://' + configs.ip + ':3232/',
				'data': {
					'action': 'getLockTime'
				},
				complete: function(resp) {
					var data = $.parseJSON(resp.getResponseHeader('data'));

					if (data != null) {
						if (data.lockTime != 0 && data.lockTime < 300000) {
							$('#alert_msg span').text(getLockTimeMessage(data.lockTime));
						} else {
							eventScreen('login');
						}
					}
				}
			});
		}
	});

	$(document).on('click', '#btn_login', function() {
		var password = $('#password').val();

		if ($.trim(password) != '') {
			$.ajax({
				'type': 'GET',
				'url': 'http://' + configs.ip + ':3232/',
				'data': {
					'action': 'login',
					'password': md5(password),
					'key': md5($.now() + password)
				},
				complete: function(resp) {
					var data = $.parseJSON(resp.getResponseHeader('data'));

					if (data != null) {
						if (data.auth) {
							$.cookie('SSID', data.key, {expires: 2});
							eventScreen('logged');
						} else {
							eventScreen('wrongCredentials', data);
							$('#password').val('');
						}
					}
				}
			});
		}
	});
}

function checkLogin() {
	var ssid = $.cookie('SSID');

	if (ssid != undefined) {
		$.ajax({
			'type': 'GET',
			'url': 'http://' + configs.ip + ':3232/',
			'data': {
				'action': 'checkLogin',
				'ssid': ssid
			},
			complete: function(resp) {
				var data = $.parseJSON(resp.getResponseHeader('data'));

				if (data != null) {
					if (data.auth) {
						eventScreen('logged');
					} else {
						eventScreen('wrongCredentials', data);
					}
				}
			}
		});
	} else {
		eventScreen('login');
	}
}

function openGate(gate) {
	var ssid = $.cookie('SSID');

	if (ssid != undefined) {
		turnOnLed(gate == 'both' ? 2500 : 1000);

		$.ajax({
			'type': 'GET',
			'url': 'http://' + configs.ip + ':3232/',
			'data': {
				'action': 'open',
				'ssid': ssid,
				'gate': gate
			},
			complete: function(resp) {
				var data = $.parseJSON(resp.getResponseHeader('data'));

				if (!data.auth) {
					eventScreen('wrongCredentials', data);
				} else {
					eventScreen('logged');
				}
			}
		});
	} else {
		eventScreen('login');
	}
}

function setConfigs(cfgs) {
	var deferredObj = $.Deferred();

	if (typeof cfgs === 'object') {
		configs = {};

		$.each(cfgs, function(key, value) {
			configs[key] = value;
		});

		deferredObj.resolve();
	} else {
		deferredObj.reject();
	}

	return deferredObj.promise();
}

function fix() {
	var el = this;
	var par = el.parentNode;
	var next = el.nextSibling;
	par.removeChild(el);
	setTimeout(function() {par.insertBefore(el, next);}, 1);
}

function turnOnLed(time) {
	$('#led').addClass('on');

	setTimeout(function() {
		$('#led').removeClass('on');
	}, time);
}

function updateStyle() {
	var deferredObj = $.Deferred();
	var width =  $('#div_remote_control').height() * 0.6;
	var border = width * 0.025;
	var btnsBorder = width * 0.01;

	$('#antena_control').css({
		'height': border + 'px',
		'left': border * 4 + 'px',
		'top' : border * -2 + 'px',
		'width': width * 0.15 + 'px',
		'border-radius': width * 0.01 + 'px ' + width * 0.01 + 'px 0 0'
	});

	$('#div_remote_control').css({
		'width': width + 'px',
		'left': (($(window).width() - (width + (border * 2))) / 2) + 'px',
		'top': (($(window).height() - ($('#div_remote_control').height() + (border * 2))) / 2) + 'px',
		'border-radius': width * 0.1,
		'border': border + 'px solid #494949'
	});

	$('.container').css({
		'padding': border * 1.5 + 'px'
	});

	$('.btns, .info-screen').css({
		'margin-bottom': border * 1.5 + 'px'
	});

	$('.info-screen').css({
		'border-radius': width * 0.02,
		'border-top-left-radius': width * 0.05,
		'border-top-right-radius': width * 0.05
	});

	$('.info-screen.login, .info-screen.question').css({
		'box-shadow': '0px 0px 0px ' + btnsBorder + 'px #124763'
	});

	$('.info-screen.logged').css({
		'box-shadow': '0px 0px 0px ' + btnsBorder + 'px #09363A'
	});

	$('.info-screen.error').css({
		'box-shadow': '0px 0px 0px ' + btnsBorder + 'px #6D1010'
	});

	$('.info-screen.alert').css({
		'box-shadow': '0px 0px 0px ' + btnsBorder + 'px #714B1C'
	});

	$('.btn, .btn-gates').css({
		'border-radius': width * 0.02,
		'box-shadow': '0px 0px 0px ' + btnsBorder + 'px #00602B',
		'font-size': width * 0.05 + 'px'
	});

	$('.btn-gates').css({
		'height': 'calc(25% - ' + (border * 3) + 'px)',
		'border-bottom-left-radius': width * 0.05,
		'border-bottom-right-radius': width * 0.05
	});

	$('#led').css({
		'width': border * 2 + 'px',
		'height': border * 2 + 'px',
		'top': 'calc(60% - ' + border + 'px)',
		'left': 'calc(50% - ' + (border * 1.5) + 'px)',
		'border-radius': '50%',
		'border': border * 0.5 + 'px solid #E2E2E2',
		'box-shadow': '0px 0px 0px ' + btnsBorder + 'px #00602B'
	});

	$('#btn_login, #btn_ok, #btn_yes, #btn_no').css({
		'border-radius': width * 0.02,
		'font-size': width * 0.05 + 'px',
		'width': '100%',
		'height': '100%'
	});

	$('#btn_login').css({
		'border': btnsBorder + 'px solid #124763',
	});

	$('#btn_ok, #btn_yes, #btn_no').css({
		'border': btnsBorder + 'px solid #525252',
	});

	$('#password').css({
		'width': '100%',
		'height': '100%',
		'border': 'none',
		'border-radius': width * 0.02,
		'padding': '0',
		'font-size': width * 0.05 + 'px',
		'text-align': 'center'
	});

	$('#login > div:nth-child(1), #alerts > div:nth-child(1)').css({
		'padding': 2 * border + 'px ' + border + 'px ' + 2 * border + 'px ' + border + 'px',
		'width': 'calc(100% - ' + 2 * border + 'px)',
		'height': 'calc(50% - ' + 4 * border + 'px)'
	});

	$('#login > div:nth-child(2), #alerts > div:nth-child(2)').css({
		'padding': border + 'px ' + ' 0 0 ' + border + 'px',
		'width': 'calc(100% - ' + 2 * border + 'px)',
		'height': 'calc(20% - ' + border + 'px)'
	});

	$('#login > div:nth-child(3), #alerts > div:nth-child(3), #alerts > div:nth-child(4)').css({
		'padding': border + 'px',
		'width': 'calc(100% - ' + 2 * border + 'px)',
		'height': 'calc(30% - ' + 2 * border + 'px)'
	});

	return deferredObj.resolve().promise();
}

function createHTML() {
	var deferredObj = $.Deferred();

	$('#div_remote_control').append(
		$('<div>', {'class': 'container'}).append(
			$('<div>', {'id': 'antena_control'}),
			$('<div>', {'class': 'info-screen'}).append(
				$('<div>', {'id': 'login', 'style': 'display: none'}).append(
					$('<div>').append(
						$('<i>', {'id': 'icon_lock', 'class': 'fa fa-lock', 'aria-hidden': 'true'})
					),
					$('<div>').append(
						$('<input>', {'type': 'password', 'id': 'password', 'name': 'password'})
					),
					$('<div>').append(
						$('<input>', {'type': 'button', 'id': 'btn_login', 'ontouchend': 'this.onclick=fix', 'value': 'LOGIN'})
					)
				),
				$('<div>', {'id': 'logged', 'style': 'display: none'}).append(
					$('<img>', {'src': 'https://raw.githubusercontent.com/lucastonus/controle-portoes/master/images/logged.gif'})
				),
				$('<div>', {'id': 'alerts', 'style': 'display: none'}).append(
					$('<div>', {'id': 'alert_icon'}),
					$('<div>', {'id': 'alert_msg'}),
					$('<div>', {'class': 'alert-btns', 'style': 'display: none'}).append(
						$('<input>', {'type': 'button', 'id': 'btn_ok', 'ontouchend': 'this.onclick=fix', 'value': 'OK / ATUALIZAR'})
					),
					$('<div>', {'class': 'alert-btns', 'style': 'display: none;'}).append(
						$('<input>', {'type': 'button', 'id': 'btn_no', 'ontouchend': 'this.onclick=fix', 'value': 'NÃO'}),
						$('<input>', {'type': 'button', 'id': 'btn_yes', 'ontouchend': 'this.onclick=fix', 'value': 'SIM'})
					)
				)
			),
			$('<div>', {'class': 'btns'}).append(
				$('<input>', {'type': 'button', 'class': 'btn', 'style': 'float: left;', 'ontouchend': 'this.onclick=fix', 'value': 'FORA', 'data-gate': 'outside'}),
				$('<input>', {'type': 'button', 'class': 'btn', 'style': 'float: right;', 'ontouchend': 'this.onclick=fix', 'value': 'DENTRO', 'data-gate': 'inside'})
			),
			$('<input>', {'type': 'button', 'class': 'btn-gates', 'style': 'float: right;', 'ontouchend': 'this.onclick=fix', 'value': 'TODOS OS PORTÕES', 'data-gate': 'both'}),
			$('<div>', {'id': 'led'})
		)
	);

	return deferredObj.resolve().promise();
}

function eventScreen(type, params) {
	params = params || false;

	$('.info-screen').removeClass('login logged error alert question');
	$('#alert_icon, #alert_msg').empty();
	$('#login, #logged, #alerts, .alert-btns').hide();

	switch (type) {
		case 'logged':
			$('.info-screen').addClass('logged');
			$('#logged').show();
			break;
		case 'wrongCredentials':
			if (params.locked) {
				var iconClass = 'fa-ban';
				var msg = getLockTimeMessage(params.lockTime);

				$('#alerts .alert-btns:eq(0) input').val('ATUALIZAR').attr('data-action', 'refresh');
				$('.info-screen').addClass('error');
			} else {
				var iconClass = 'fa-exclamation-triangle';
				var msg = 'Você tem mais ' + (params.attempts < 5 ? (5 - params.attempts) : 0) + ' tentativas.';

				$('#alerts .alert-btns:eq(0) input').val('OK').attr('data-action', 'ok');
				$('.info-screen').addClass('alert');
			}
			$('#alerts .alert-btns:eq(0)').show();
			$('#alerts').show();
			break;
		case 'login':
			$('.info-screen').addClass('login');
			$('#login').show();
			break;
		case 'question':
			$('.info-screen').addClass('question');

			var iconClass = 'fa-question-circle';
			var msg = 'Deseja realmente abrir?';
			$('#btn_yes').attr('data-gate', params.gate);
			$('#alerts .alert-btns:eq(1)').show();
			$('#alerts').show();
			break;
	}

	if (iconClass != '' && msg != '') {
		$('#alert_icon').append(
			$('<i>', {'class': 'icon fa ' + iconClass})
		);

		var fontSize = $('#div_remote_control').height() * 0.03 + 'px';
		$('#alert_msg').append(
			$('<span>', {'text': msg, 'style': 'font-size: ' + fontSize})
		);
	}

	updateStyle();
}

function getLockTimeMessage(time) {
	if (time > 300000) {
		time = 0;
	} else {
		time = 300000 - time;
	}

	var minutes = Math.floor(time / 60000);
	var seconds = ((time % 60000) / 1000).toFixed(0);
	var formatedTime = minutes + ':' + (seconds < 10 ? '0' : '') + (seconds < 60 ? seconds : 59);

	return 'Aguarde ' + formatedTime + ' e tente novamente.';
}