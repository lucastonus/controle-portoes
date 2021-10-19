#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <ArduinoHttpClient.h>

const String ssid = "";
const String wifiPassword = "";

const String wsAddress = "";
const int wsPort = 7777;

WiFiClient wifiClient;
WebSocketClient wsc = WebSocketClient(wifiClient, wsAddress, wsPort);

int gateOutside = D1;
int gateInside = D2;
int led = D8;

const int GATE_OUTSIDE = 1;
const int GATE_INSIDE = 2;
const int GATE_BOTH = 3;

void setup() {
	Serial.begin(115200);
	initPins();
	connectWifi();
	wsc.begin();
}

void loop() {
	while (wsc.connected()) {
		if (wsc.parseMessage()) {
			String payload = wsc.readString();

			Serial.println(payload);

			DynamicJsonDocument message(1024);
			DeserializationError error = deserializeJson(message, payload);

			if (!error) {
				int gate = message["gate"];

				switch (gate) {
					case GATE_OUTSIDE:
						Serial.println("Abrindo portão: OUTSIDE");
						openGate(gateOutside);
						break;
					case GATE_INSIDE:
						Serial.println("Abrindo portão: INSIDE");
						openGate(GATE_INSIDE);
						break;
					case GATE_BOTH:
						Serial.println("Abrindo portão: OUTSIDE e INSIDE");
						openGate(gateOutside);
						openGate(GATE_INSIDE);
						break;
				}
			}
		}
	}
}

void connectWifi() {
	WiFi.begin(ssid, wifiPassword);

	while (WiFi.status() != WL_CONNECTED) {
		digitalWrite(led, HIGH);
		delay(500);
		digitalWrite(led, LOW);
		delay(500);
	}
}

void initPins() {
	pinMode(gateOutside, OUTPUT);
	pinMode(gateInside, OUTPUT);
	pinMode(led, OUTPUT);
	digitalWrite(gateOutside, HIGH);
	digitalWrite(gateInside, HIGH);
	digitalWrite(led, HIGH);
}

void openGate(int gate) {
	digitalWrite(led, HIGH);
	// digitalWrite(gate, HIGH);
	delay(750);
	// digitalWrite(gate, LOW);
	digitalWrite(led, LOW);
	delay(750);
}