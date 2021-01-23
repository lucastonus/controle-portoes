#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <ArduinoHttpClient.h>

const String ssid = "";
const String wifiPassword = "";

const String wsAddress = "";
const int wsPort = 8888;

WiFiClient wifiClient;
WebSocketClient wsc = WebSocketClient(wifiClient, wsAddress, wsPort);

int gateOutside = D1;
int gateInside = D2;
int led = D8;

const int GATE_OUTSIDE = 1;
const int GATE_INSIDE = 2;

void setup() {
	Serial.begin(115200);
	initPins();
	connectWifi();
	wsc.begin();
}

void loop() {
	while (wsc.connected()) {
		if (wsc.parseMessage() > 0) {
			DynamicJsonDocument message(1024);

			String payload = wsc.readString();
			Serial.println(payload);

			deserializeJson(message, payload);

			for (int i = 0; i < int(message["gates"]["length"]); i++) {
				digitalWrite(led, HIGH);

				int gate = getGate(message["gates"]["gate"][i]);

				switch (gate) {
					case GATE_OUTSIDE:
						Serial.println("Abrindo portão: OUTSIDE");
						// digitalWrite(gateOutside, LOW);
						// delay(1000);
						// digitalWrite(gateOutside, HIGH);
						break;
					case GATE_INSIDE:
						Serial.println("Abrindo portão: INSIDE");
						// digitalWrite(gateInside, LOW);
						// delay(1000);
						// digitalWrite(gateInside, HIGH);
						break;
				}

				delay(500);
				digitalWrite(led, LOW);
				delay(500);
			}
		}
	}
}

void connectWifi() {
	WiFi.begin(ssid, wifiPassword);

	while (WiFi.status() != WL_CONNECTED) {
		digitalWrite(led, LOW);
		delay(500);
		digitalWrite(led, HIGH);
		delay(500);
	}

	digitalWrite(led, LOW);
}

void initPins() {
	pinMode(gateOutside, OUTPUT);
	pinMode(gateInside, OUTPUT);
	pinMode(led, OUTPUT);
	digitalWrite(gateOutside, HIGH);
	digitalWrite(gateInside, HIGH);
	digitalWrite(led, HIGH);
}

int getGate(String gate) {
	if (!gate.compareTo(String("GATE_OUTSIDE"))) {
		return GATE_OUTSIDE;
	} else if (!gate.compareTo(String("GATE_INSIDE"))) {
		return GATE_INSIDE;
	}
}