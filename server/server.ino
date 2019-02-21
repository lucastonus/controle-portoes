#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

#define LENGTH 50
#define ATTEMPTS_LIMIT 5

const char* ssid = "wifi-ssid";
const char* wifiPassword = "wifi-password";
const char* password = "md5-password";
const char* ip = "external-ip-address";
WiFiServer wifiServer(8080);

struct Attempts {
	int ip;
	int time;
	int count;
};
Attempts attempts[LENGTH];

unsigned long militime;
char key[33] = "";
int pFora = D1;
int pDentro = D2;
int led = D8;
int running = 1;

void setup() {
	Serial.begin(115200);
	initWifi();
	initPins();
	initList();
	fadeLed();
}

void loop() {
	militime = millis();
	keyExpires();
	freeAttempts();

	WiFiClient client = wifiServer.available();

	if (!client || !running) {
		return;
	}

	String request = client.readStringUntil('\r');
	request.replace("GET /?", "");
	request.replace(" HTTP/1.1", "");
	request.replace("=", "': '");
	request.replace("&", "', '");
	request = "{'" + request + "'}";

	DynamicJsonBuffer jBuffer;
	JsonObject& jObject = jBuffer.parseObject(request);
	String action = jObject["action"];

	if (action == "login") {
		String jPassword = jObject["password"];
		String jKey = jObject["key"];

		if (jPassword == password) {
			client.println("HTTP/1.1 200 OK");
			client.println("Content-Type: application/json");

			if (strcmp(key, "") == 0) {
				jKey.toCharArray(key, 33);
				client.println("data: {\"auth\": true, \"key\": \"" + jKey + "\"}");
			} else {
				client.println("data: {\"auth\": true, \"key\": \"" + String(key) + "\"}");
			}
		} else {
			wrongCredentials(client);
		}
	} else if (action == "checkLogin") {
		String jSSID = jObject["ssid"];

		if (jSSID == key && jSSID != "") {
			client.println("HTTP/1.1 200 OK");
			client.println("Content-Type: application/json");
			client.println("data: {\"auth\": true}");
		} else {
			wrongCredentials(client);
		}
	} else if (action == "open") {
		String jSSID = jObject["ssid"];
		String jGate = jObject["gate"];

		if (jSSID == key) {
			client.println("HTTP/1.1 200 OK");
			client.println("Content-Type: application/json");
			client.println("data: {\"auth\": true}");

			int gate = 0;

			if (jGate == "outside") {
				gate = 1;
			} else if (jGate == "inside") {
				gate = 2;
			} else if (jGate == "both") {
				gate = 3;
			}

			switch (gate) {
				case 1:
					digitalWrite(led, HIGH);
					digitalWrite(pFora, LOW);
					delay(1000);
					digitalWrite(pFora, HIGH);
					digitalWrite(led, LOW);
					break;
				case 2:
					digitalWrite(led, HIGH);
					digitalWrite(pDentro, LOW);
					delay(1000);
					digitalWrite(pDentro, HIGH);
					digitalWrite(led, LOW);
					break;
				case 3:
					digitalWrite(led, HIGH);
					digitalWrite(pFora, LOW);
					delay(1000);
					digitalWrite(pFora, HIGH);
					delay(500);
					digitalWrite(pDentro, LOW);
					delay(1000);
					digitalWrite(pDentro, HIGH);
					digitalWrite(led, LOW);
					break;
			}
		} else {
			wrongCredentials(client);
		}
	} else if (action == "getLockTime") {
		int iLocked = isLocked(client);
		int lockTime = 0;

		if (iLocked != -1) {
			lockTime = militime - attempts[iLocked].time;
		}

		client.println("HTTP/1.1 200 OK");
		client.println("Content-Type: application/json");
		client.println("data: {\"lockTime\": " + String(lockTime) + "}");
	}

	delay(10);

	client.println("HTTP/1.1 200 OK");
	client.println("Content-Type: text/html");
	client.println("");
	client.println("<!DOCTYPE HTML><html><head><meta charset='utf-8'><title>Controle dos Portões</title><link rel='stylesheet' type='text/css' href='https://rawgit.com/lucastonus/controle-portoes/master/style.css'></head><body><div id='div_remote_control' style='display: none;'></div></body></html><script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script><script src='https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.js'></script><script src='https://cdnjs.cloudflare.com/ajax/libs/blueimp-md5/2.10.0/js/md5.js'></script><script defer src='https://use.fontawesome.com/releases/v5.0.9/js/all.js' integrity='sha384-8iPTk2s/jMVj81dnzb/iFR2sdA7u06vHJyyLlAd4snFpCl/SnyUjRrbdJsw1pGIl' crossorigin='anonymous'></script><script src='https://rawgit.com/lucastonus/controle-portoes/master/script.js'></script>");
	client.println("<script>var promiseObj=setConfigs({'ip':'" + String(ip) + "'});promiseObj.done(function(){init();});</script>");
}

void initWifi() {
	WiFi.mode(WIFI_STA);
	IPAddress ip(192, 168, 0, 32);
	IPAddress subnet(255, 255, 255, 0);
	IPAddress gateway(192, 168, 0, 1);
	WiFi.config(ip, gateway, subnet);
	WiFi.begin(ssid, wifiPassword);

	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
	}

	wifiServer.begin();
}

void initPins() {
	pinMode(pFora, OUTPUT);
	pinMode(pDentro, OUTPUT);
	pinMode(led, OUTPUT);
	digitalWrite(pFora, HIGH);
	digitalWrite(pDentro, HIGH);
	digitalWrite(led, LOW);
}

void initList() {
	for (int i = 0; i < LENGTH; i++) {
		attempts[i].ip = 0;
		attempts[i].time = 0;
		attempts[i].count = 0;
	}
}

void fadeLed() {
	for (int i = 0; i < 5; i++) {
		digitalWrite(led, HIGH);
		delay(1000);
		digitalWrite(led, LOW);
		delay(500);
	}
}

void wrongCredentials(WiFiClient client) {
	int i = addAttempt(client);
	int lockTime = 0;

	if (attempts[i].count >= ATTEMPTS_LIMIT) {
		lockTime = militime - attempts[i].time;
	}

	client.println("HTTP/1.1 401 ERRO DE CREDENCIAIS");
	client.println("Content-Type: application/json");
	client.println("data: {\"auth\": false, \"locked\":" + String(attempts[i].count >= ATTEMPTS_LIMIT) + ", \"attempts\":" + String(attempts[i].count) + ", \"lockTime\":" + String(lockTime) + "}");
}

void keyExpires() {
	if (militime % 604800000 == 0) {
		strcpy(key, "");
	}
}

void freeAttempts() {
	if (militime % 5000 == 0) {
		for (int i = 0; i < LENGTH; i++) {
			if ((militime - attempts[i].time) > 300000) {
				attempts[i].ip = 0;
				attempts[i].time = 0;
				attempts[i].count = 0;
			}
		}
	}
}

int addAttempt(WiFiClient client) {
	int found = 0;
	int iReplace = 0;
	int res = 0;
	String ip = client.remoteIP().toString();
	ip.replace(".", "");

	for (int i = 0; i < LENGTH && !found; i++) {
		if (attempts[i].ip == ip.toInt()) {
			found = 1;
			attempts[i].count++;
			if (attempts[i].count == 5) {
				attempts[i].time = militime;
			}
			res = i;
		}
	}

	for (int i = 0; i < LENGTH && !found; i++) {
		if (!attempts[i].ip) {
			found = 1;
			attempts[i].ip = ip.toInt();
			attempts[i].count++;
			res = i;
		}

		if (attempts[i].count <= attempts[iReplace].count && i != iReplace) {
			if (attempts[i].count == attempts[iReplace].count) {
				if (attempts[i].time <= attempts[iReplace].time) {
					iReplace = i;
				}
			} else {
				iReplace = i;
			}
		}
	}

	if (!found) {
		attempts[iReplace].ip = ip.toInt();
		attempts[iReplace].time = militime;
		attempts[iReplace].count = 1;
		running = 0;
		res = iReplace;
	}

	return res;
}

void showList() {
	if (militime % 5000 == 0) {
		Serial.println("################");
		for (int i = 0; i < LENGTH; i++) {
			Serial.println("----------------");
			Serial.print("i: ");
			Serial.println(i);
			Serial.print("IP: ");
			Serial.println(attempts[i].ip);
			Serial.print("Time: ");
			Serial.println(attempts[i].time);
			Serial.print("Count: ");
			Serial.println(attempts[i].count);
		}
	}
}

int isLocked(WiFiClient client) {
	int res = -1;
	String ip = client.remoteIP().toString();
	ip.replace(".", "");

	for (int i = 0; i < LENGTH; i++) {
		if (attempts[i].ip == ip.toInt() && attempts[i].count >= 5) {
			res = i;
		}
	}

	return res;
}